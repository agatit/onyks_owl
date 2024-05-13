from dataclasses import dataclass
from tkinter import Variable
from typing import Literal, Any

from selector.tracing.TraceCallable import TraceCallable

TraceMode = Literal["array", "read", "write", "unset"]


@dataclass
class TraceData:
    id_: int
    name: str
    mode: TraceMode


class VarRegister:

    def __init__(self):
        self._vars: dict[str, Variable] = {}
        self._traces: dict[str, dict[str, TraceData]] = {}

    def add_var(self, var_name: str, var: Variable) -> None:
        if var_name not in self._vars:
            self._vars[var_name] = var
            self._traces[var_name] = {}

    def get_var_value(self, var_name: str) -> Any:
        # todo: zmiana na dekorator
        if var_name not in self._vars:
            raise ValueError(f"Variable {var_name} does not exist")

        return self._vars[var_name].get()

    def trace_add(self, var_name: str, trace_name: str, mode: TraceMode, callback: TraceCallable):
        if var_name not in self._vars:
            raise ValueError(f"Variable {var_name} does not exist")

        var = self._vars[var_name]
        traces = self._traces[var_name]

        trace_id = var.trace_add(mode, callback)
        trace_data = TraceData(trace_id, trace_name, mode)
        traces[trace_name] = trace_data

    def trace_remove(self, var_name: str, trace_name: str):
        if var_name not in self._vars:
            raise ValueError(f"Variable {var_name} does not exist")

        if trace_name not in self._traces[var_name]:
            raise ValueError(f"Trace {trace_name} does not exist")

        var = self._vars[var_name]
        trace = self._traces[var_name][trace_name]

        var.trace_remove(trace.mode, trace.id_)
        del self._traces[var_name][trace_name]


def trace_add(register: VarRegister, var_name: str, mode: TraceMode, trace_name: str, callback: TraceCallable):
    register.trace_add(var_name, trace_name, mode, callback)
