import os
import sys
import json
import logging
import cv2
import redis
import task
import stream_video
import stream_data
import module_base
from urllib.parse import urljoin
import m3u8
import av
import pafy
import time
from datetime import datetime, timedelta

logging.getLogger('libav').setLevel(logging.ERROR)

class Module(module_base.Module):

    last_segment = None
    last_segment_time = None

    def setup(self): 
        self.input_classes = {}
        self.output_classes = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer
        }

    def get_segment(self, url):

        m3u8_obj = m3u8.load(url)    
        segment = m3u8_obj.segments[-1] #domyślnie najnowszy
        segment_no = len(m3u8_obj.segments)-1
        
        if self.last_segment:                                      
            # bieżący segment jest najnowszy - oczekiwanie na nowy            
            while m3u8_obj.segments[-1].uri == self.last_segment.uri:
                sleep_time = 0.1
                if self.last_segment_time:
                    sleep_time = self.last_segment.duration - (datetime.now() - self.last_segment_time).total_seconds() + 0.1
                if sleep_time <= 0:
                    sleep_time = 0.1
                logging.warning(f"Need to wait for segment {sleep_time}s")
                time.sleep(sleep_time)
                m3u8_obj = m3u8.load(url)

            # szukanie segmentu następnego
            segment = None
            for i in range(len(m3u8_obj.segments)-1):
                if m3u8_obj.segments[i].uri == self.last_segment.uri: # może lepiej sprawdzać po czasie?
                    segment_no = i+1
                    segment = m3u8_obj.segments[segment_no]                    
                    break
            
            if not segment:
                segment_no = 0
                segment = m3u8_obj.segments[segment_no]                

                # sprawdzenie ciągłości
                if self.last_segment.current_program_date_time \
                        and self.last_segment.duration \
                        and segment.current_program_date_time \
                        and segment.current_program_date_time  \
                            - (self.last_segment.current_program_date_time \
                            + timedelta(seconds=self.last_segment.duration)) \
                            > timedelta(seconds=1):
                    logging.error(f"Segment(s) lost from {self.last_segment.current_program_date_time + timedelta(seconds=self.last_segment.duration)} to {segment.current_program_date_time}")                        
                    self.last_segment = None
                    return None, -1             

        self.last_segment = segment  
        if self.last_segment_time:
            measured_time = (datetime.now() - self.last_segment_time).total_seconds()
        else:
            measured_time = 0
        logging.debug(f"{segment_no}/{len(m3u8_obj.segments)} {segment.current_program_date_time} {segment.duration} ({measured_time:.1f})")
        self.last_segment_time = datetime.now()
        
        return segment, len(m3u8_obj.segments) - segment_no - 1


    def task_process(self, input_task_data, input_stream):
        'przetwarzanie strumieni'
        output_task_data = {}

        output_task_data['source_name'] = self.params.get('source_name',self.last_segment.title)
        with self.task_emit(output_task_data) as output_stream:
            
            while True:                
                segment, segments_left = self.get_segment(self.params['url'])
                if not segment:                    
                    return

                # dekodowanie
                video_url = urljoin(self.params['url'], segment.uri)
                video_av = av.open(video_url, "r")
                video_av.streams.video[0].thread_type = 'AUTO'
    
                for frame in video_av.decode(video=0):
                    img = frame.to_ndarray(format="bgr24")
                    data = {
                        'color' : img,
                        'metrics' : {}
                    }
                    output_stream.emit(data)



if __name__ == "__main__":
    module = Module.from_cmd(sys.argv)
    module.run()