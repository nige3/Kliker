"""
Thread-safe state management for Kliker auto-clicker.
Encapsulates all shared state and provides synchronized access.
"""

import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple, Optional


@dataclass
class ClickerState:
    """Thread-safe state container for clicker operations."""

    # Thread synchronization
    _lock: threading.RLock = field(default_factory=threading.RLock)

    # Clicking state
    is_running: bool = False
    click_thread: Optional[threading.Thread] = None

    # Hotkey and recording
    hotkey_listener: Optional[object] = None
    record_mode: bool = False
    record_listener: Optional[object] = None

    # Recorded positions for sequence mode
    recorded_positions: List[Tuple[int, int]] = field(default_factory=list)

    # Session statistics
    total_clicks: int = 0
    session_start: Optional[datetime] = None
    last_click_time: Optional[datetime] = None
    clicks_per_minute: float = 0.0

    # Operating mode
    current_mode: str = "realtime"  # "realtime" or "sequence"

    def __enter__(self):
        """Context manager entry - acquire lock."""
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - release lock."""
        self._lock.release()

    def set_running(self, value: bool) -> None:
        """Safely set running state."""
        with self._lock:
            self.is_running = value

    def get_running(self) -> bool:
        """Safely get running state."""
        with self._lock:
            return self.is_running

    def increment_clicks(self) -> int:
        """Safely increment click counter and return new value."""
        with self._lock:
            self.total_clicks += 1
            self.last_click_time = datetime.now()
            return self.total_clicks

    def get_total_clicks(self) -> int:
        """Safely get total clicks."""
        with self._lock:
            return self.total_clicks

    def set_click_thread(self, thread: Optional[threading.Thread]) -> None:
        """Safely set click thread reference."""
        with self._lock:
            self.click_thread = thread

    def get_click_thread(self) -> Optional[threading.Thread]:
        """Safely get click thread reference."""
        with self._lock:
            return self.click_thread

    def add_position(self, x: int, y: int) -> None:
        """Safely add recorded position."""
        with self._lock:
            self.recorded_positions.append((x, y))

    def get_positions(self) -> List[Tuple[int, int]]:
        """Safely get copy of recorded positions."""
        with self._lock:
            return list(self.recorded_positions)

    def clear_positions(self) -> None:
        """Safely clear recorded positions."""
        with self._lock:
            self.recorded_positions.clear()

    def get_positions_count(self) -> int:
        """Safely get count of recorded positions."""
        with self._lock:
            return len(self.recorded_positions)

    def set_hotkey_listener(self, listener: Optional[object]) -> None:
        """Safely set hotkey listener."""
        with self._lock:
            self.hotkey_listener = listener

    def get_hotkey_listener(self) -> Optional[object]:
        """Safely get hotkey listener."""
        with self._lock:
            return self.hotkey_listener

    def set_record_listener(self, listener: Optional[object]) -> None:
        """Safely set record listener."""
        with self._lock:
            self.record_listener = listener

    def get_record_listener(self) -> Optional[object]:
        """Safely get record listener."""
        with self._lock:
            return self.record_listener

    def set_record_mode(self, value: bool) -> None:
        """Safely set record mode."""
        with self._lock:
            self.record_mode = value

    def get_record_mode(self) -> bool:
        """Safely get record mode."""
        with self._lock:
            return self.record_mode

    def reset_session(self) -> None:
        """Reset session statistics."""
        with self._lock:
            self.total_clicks = 0
            self.session_start = datetime.now()
            self.last_click_time = None
            self.clicks_per_minute = 0.0

    def calculate_cpm(self) -> float:
        """Calculate clicks per minute safely."""
        with self._lock:
            if not self.session_start or self.total_clicks == 0:
                return 0.0

            elapsed = (datetime.now() - self.session_start).total_seconds()
            if elapsed > 0:
                return (self.total_clicks / elapsed) * 60
            return 0.0

    def get_stats_snapshot(self) -> dict:
        """Get snapshot of current statistics."""
        with self._lock:
            return {
                'total_clicks': self.total_clicks,
                'clicks_per_minute': self.calculate_cpm(),
                'is_running': self.is_running,
                'mode': self.current_mode,
                'recorded_positions': len(self.recorded_positions)
            }
