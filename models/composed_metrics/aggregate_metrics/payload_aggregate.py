from dataclasses import dataclass, field

@dataclass
class PayloadVersion:
    """For a single version"""
    timing_delays_count: int = 0
    eval_count: int = 0
    shell_commands_count: int = 0
    preinstall_scripts: list[str] = field(default_factory=list)

@dataclass
class PayloadAggregate:
    """For aggregate versions"""
    avg_timing_delays_count: int = 0
    avg_eval_count: int = 0
    avg_shell_commands_count: int = 0