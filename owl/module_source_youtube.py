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
import m3u8
import av
import pafy
import time
from datetime import datetime



class Module(module_base.Module):

    def streams_init(self): 
        self.input_classes = {}
        self.output_classes = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer
        }

        self.last_program_date_time =  None
        self.next_frame = time.time()


    def task_process(self, input_task_data, input_stream):
        'przetwarzanie strumieni'

        stream_name = self.params.get('stream', 'best')
        video = pafy.new(self.params['url'])
        logging.info(f"Streams availaible: {video.streams}")
        
        if stream_name == "best":
            stream = video.getbest(preftype="mp4")
        else:
            stream = next(s for s in video.streams if str(s)==self.params['stream'])        

        frame_time = 1/int(stream._info['fps'])

        with self.task_emit({}) as output_stream:
            while True:                
                if stream._info['protocol'] == 'm3u8':
                    realtime = True
                    m3u8_obj = m3u8.load(stream.url)
                    stream_segment = m3u8_obj.segments[0]
                    if self.last_program_date_time == None:
                        last_program_date_time = stream_segment.program_date_time
                    elif stream_segment.program_date_time > last_program_date_time + m3u8_obj.targetduration:
                        logging.warning("Lost segment")
                    elif stream_segment.program_date_time <= last_program_date_time:                       
                        logging.warning("Need to wait for segment")
                        time.sleep(frame_time)
                        continue
                    last_program_date_time = stream_segment.program_date_time
                    video_url = stream_segment.uri
                else:
                    realtime = False # może wymusić realtime też dla normalnych?
                    video_url = stream.url

                video_av = av.open(video_url, "r")
    
                for frame in video_av.decode(video=0):
                    img = frame.to_ndarray(format="bgr24")
                    data = {
                        'color' : img,
                        'metrics' : {}
                    }
                    output_stream.emit(data)

                    self.next_frame += frame_time
                    if realtime and time.time() < self.next_frame:
                        time.sleep(self.next_frame - time.time())


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()