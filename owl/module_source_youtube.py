import sys
import logging
import stream_video
import stream_data
import module_source_m3u8
from urllib.parse import urljoin
import av
import pafy
import time


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
        
        return stream, video._title        

    def task_process(self, input_task_data, input_stream):
        'przetwarzanie strumieni'

        stream, title = self.get_youtube_stream(self.params['url'], self.params.get('stream', 'best'))
        frame_time = 1/int(stream._info['fps'])
        

        output_task_data = {}

        output_task_data['source_name'] = self.params.get('name', title)
        with self.task_emit(output_task_data) as output_stream:

            while True:                   
                next_frame =  time.time()

                if stream._info['protocol'] == 'm3u8':
                    realtime = self.params.get("realtime", True) # można wymusić realtime też dla normalnych
                    segment, segments_left = self.get_segment(stream.url)
                    if not segment:
                        return
                    video_url = urljoin(self.params['url'], segment.uri)
                else:
                    realtime = self.params.get("realtime", False) # można wymusić realtime też dla normalnych
                    segments_left = 1 #aby działał realtime dla normalnych
                    video_url = stream.url
                
                # dekodowanie              
                with av.open(video_url, "r") as video_av:
                    video_av.streams.video[0].thread_type = 'FRAME'
                    video_av.streams.video[0].thread_count = 10
        
                    for frame in video_av.decode(video=0):                    
                        img = frame.to_ndarray(format="bgr24")
                        data = {
                            'color' : img,
                            'metrics' : {}
                        }
                        output_stream.emit(data)

                        next_frame += frame_time * 0.99 # setna cześć klatki wyprzedzenia
                        now = time.time()
                        if realtime and segments_left == 0 and now < next_frame:
                            time.sleep(next_frame - now)


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()