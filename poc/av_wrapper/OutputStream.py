from dataclasses import dataclass, field
from fractions import Fraction

from av import VideoFrame
from av.video.stream import VideoStream
from torchvision.io.video import av

from av_wrapper.Stream import Stream


@dataclass(kw_only=True)
class OutputStream(Stream):
    width: int
    height: int
    fps: Fraction

    pixel_format: str = "yuv420p"
    codec: str = "mpeg4"

    _out_container: any = field(init=False, default=None)
    _out_stream: VideoStream = field(init=False, default=None)

    def open(self) -> None:
        out_cont = av.open(self.movie_path, mode="w")

        out_stream: VideoStream = out_cont.add_stream(self.codec, rate=self.fps)
        out_stream.width = self.width
        out_stream.height = self.height
        out_stream.pix_fmt = self.pixel_format

        self._out_container = out_cont
        self._out_stream = out_stream

    def write(self, raw_frame: VideoFrame) -> None:
        if self._out_container is None:
            raise Exception("Output stream is not open")

        np_frame = raw_frame.to_ndarray(format="rgb24")
        frame = av.VideoFrame.from_ndarray(np_frame, format="rgb24")

        out_container = self._out_container
        for packet in self._out_stream.encode(frame):
            packet.dts = raw_frame.dts
            packet.pts = raw_frame.pts
            packet.time_base = raw_frame.time_base
            out_container.mux(packet)

    def close(self) -> None:
        if self._out_container is None:
            return

        out_container = self._out_container
        for packet in self._out_stream.encode():
            out_container.mux(packet)

        self._out_container.close()
