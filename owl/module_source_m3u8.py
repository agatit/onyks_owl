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

    def streams_init(self): 
        self.input_classes = {}
        self.output_classes = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer
        }

    def get_segment(self, url):

        m3u8_obj = m3u8.load(url)    
        stream_segment = m3u8_obj.segments[-1] #domyślnie najnowszy
        segment_no = 0

        # wybór segmentu
        if self.last_segment:                                      
            for i in range(len(m3u8_obj.segments)):
                if m3u8_obj.segments[i].uri == self.last_segment.uri:
                    if i+1 < len(m3u8_obj.segments):
                        stream_segment = m3u8_obj.segments[i+1]
                        segment_no = i+1
                    else:
                        stream_segment = None                            
                    break                      

        # oczekiwanie na nowy            
        if not stream_segment:
            logging.warning("Need to wait for segment")
            time.sleep(0.02)
            return None        

        # sprawdzenie ciągłości
        if self.last_segment \
                and self.last_segment.current_program_date_time \
                and self.last_segment.duration \
                and stream_segment.current_program_date_time \
                and stream_segment.current_program_date_time  \
                    - (self.last_segment.current_program_date_time \
                    + timedelta(seconds=self.last_segment.duration)) \
                    > timedelta(seconds=1):
            logging.error(f"Segment(s) lost from {self.last_segment.current_program_date_time + timedelta(seconds=self.last_segment.duration)} to {stream_segment.current_program_date_time}")

        logging.debug(f"{segment_no}/{len(m3u8_obj.segments)} {stream_segment.current_program_date_time} {stream_segment.duration}")
        return stream_segment



    def task_process(self, input_task_data, input_stream):
        'przetwarzanie strumieni'

        with self.task_emit({}) as output_stream:
            
            while True:                
                stream_segment = self.get_segment(self.params['url'])
                if not stream_segment:
                    break

                # dekodowanie
                video_url = urljoin(self.params['url'], stream_segment.uri)
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
    module = Module(sys.argv)
    module.run()