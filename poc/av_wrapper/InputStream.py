from dataclasses import dataclass, field

import av
from av import VideoFrame
from av.video.stream import VideoStream

from av_wrapper.Stream import Stream


@dataclass(kw_only=True)
class InputStream(Stream):
    video_stream_index: int = 0

    def __post_init__(self):
        av_container = av.open(self.movie_path)
        video_stream: VideoStream = av_container.streams.video[self.video_stream_index]

        self.width = video_stream.width
        self.height = video_stream.height
        self.fps = video_stream.base_rate

        self.pixel_format = video_stream.format.name
        self.codec = video_stream.codec_context.name

        av_container.close()

    def open(self) -> VideoFrame:
        av_container = av.open(self.movie_path)
        self.frame_counter = 0

        for raw_frame in av_container.decode(video=self.video_stream_index):
            yield raw_frame
            self.frame_counter += 1

        av_container.close()
