import os
import sys
import json
import logging
import cv2
import redis
import task
import stream_video
import stream_data
import module_source_m3u8
from urllib.parse import urljoin
import m3u8
import av
import pafy
import time
from datetime import datetime


class Module(module_source_m3u8.Module):

    def streams_init(self): 
        self.input_classes = {}
        self.output_classes = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer
        }

    def get_youtube_stream(self, url, stream_name="best"):
        # odczytanie strumienia YT
        video = pafy.new(url, {"--no-check-certificate": True})
        logging.info(f"Streams availaible: {video.streams}")        
        if stream_name == "best":
            stream = video.getbest(preftype="mp4")
        else:
            stream = next(s for s in video.streams if str(s)==stream_name)        
        
        return stream         

    def task_process(self, input_task_data, input_stream):
        'przetwarzanie strumieni'

        stream = self.get_youtube_stream(self.params['url'], self.params.get('stream', 'best'))
        frame_time = 1/int(stream._info['fps'])
        

        with self.task_emit({}) as output_stream:

            while True:                   
                next_frame =  time.time()

                if stream._info['protocol'] == 'm3u8':
                    realtime = self.params.get("realtime", True) # można wymusić realtime też dla normalnych
                    stream_segment = self.get_segment(stream.url)
                    if not stream_segment:
                        continue
                    video_url = urljoin(self.params['url'], stream_segment.uri)
                else:
                    realtime = self.params.get("realtime", False) # można wymusić realtime też dla normalnych
                    video_url = stream.url
                
                # dekodowanie               
                video_av = av.open(video_url, "r")
                video_av.streams.video[0].thread_type = 'AUTO'
    
                for frame in video_av.decode(video=0):                    
                    img = frame.to_ndarray(format="bgr24")
                    data = {
                        'color' : img,
                        'metrics' : {}
                    }
                    output_stream.emit(data)

                    next_frame += frame_time * 0.99 # setna cześć klatki wyprzedzenia
                    if realtime and time.time() < next_frame:
                        time.sleep(next_frame - time.time())


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()