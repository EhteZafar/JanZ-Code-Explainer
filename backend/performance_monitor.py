"""
Performance Metrics and Monitoring System
Tracks response times, accuracy, and system health
"""

import time
import logging
from typing import Dict, List, Optional
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """
    Monitor and track performance metrics for the AI Code Explainer.
    """
    
    def __init__(self, max_history: int = 1000):
        """
        Initialize performance monitor.
        
        Args:
            max_history: Maximum number of requests to keep in history
        """
        self.max_history = max_history
        self.request_history = deque(maxlen=max_history)
        self.start_time = datetime.now()
        
        # Metrics
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_response_time = 0.0
        self.rag_requests = 0
        self.basic_requests = 0
        
        logger.info("Performance monitor initialized")
    
    def record_request(
        self,
        mode: str,
        response_time: float,
        success: bool,
        code_length: int,
        retrieved_count: int = 0,
        error: Optional[str] = None
    ) -> None:
        """
        Record a request for metrics tracking.
        
        Args:
            mode: 'basic' or 'rag'
            response_time: Time taken to process request (seconds)
            success: Whether request was successful
            code_length: Length of input code
            retrieved_count: Number of documents retrieved (RAG mode)
            error: Error message if failed
        """
        self.total_requests += 1
        
        if success:
            self.successful_requests += 1
            self.total_response_time += response_time
        else:
            self.failed_requests += 1
        
        if mode == 'rag':
            self.rag_requests += 1
        else:
            self.basic_requests += 1
        
        # Add to history
        self.request_history.append({
            'timestamp': datetime.now().isoformat(),
            'mode': mode,
            'response_time': response_time,
            'success': success,
            'code_length': code_length,
            'retrieved_count': retrieved_count,
            'error': error
        })
        
        logger.info(
            f"Request recorded: mode={mode}, "
            f"time={response_time:.2f}s, success={success}"
        )
    
    def get_statistics(self) -> Dict:
        """
        Get comprehensive performance statistics.
        
        Returns:
            Dictionary with performance metrics
        """
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        # Calculate averages
        avg_response_time = (
            self.total_response_time / self.successful_requests
            if self.successful_requests > 0
            else 0
        )
        
        success_rate = (
            (self.successful_requests / self.total_requests * 100)
            if self.total_requests > 0
            else 0
        )
        
        rag_usage_rate = (
            (self.rag_requests / self.total_requests * 100)
            if self.total_requests > 0
            else 0
        )
        
        # Recent performance (last 10 requests)
        recent_requests = list(self.request_history)[-10:]
        recent_response_times = [
            r['response_time'] for r in recent_requests if r['success']
        ]
        recent_avg_time = (
            sum(recent_response_times) / len(recent_response_times)
            if recent_response_times
            else 0
        )
        
        return {
            'system': {
                'uptime_seconds': round(uptime, 2),
                'uptime_formatted': self._format_uptime(uptime),
                'start_time': self.start_time.isoformat()
            },
            'requests': {
                'total': self.total_requests,
                'successful': self.successful_requests,
                'failed': self.failed_requests,
                'success_rate': round(success_rate, 2)
            },
            'performance': {
                'avg_response_time': round(avg_response_time, 3),
                'recent_avg_response_time': round(recent_avg_time, 3),
                'total_response_time': round(self.total_response_time, 2)
            },
            'modes': {
                'rag_requests': self.rag_requests,
                'basic_requests': self.basic_requests,
                'rag_usage_rate': round(rag_usage_rate, 2)
            },
            'health': {
                'status': self._get_health_status(),
                'warnings': self._get_warnings()
            }
        }
    
    def _format_uptime(self, seconds: float) -> str:
        """Format uptime as human-readable string."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"
    
    def _get_health_status(self) -> str:
        """Determine system health status."""
        if self.total_requests == 0:
            return 'idle'
        
        success_rate = (
            self.successful_requests / self.total_requests * 100
        )
        
        if success_rate >= 95:
            return 'healthy'
        elif success_rate >= 80:
            return 'degraded'
        else:
            return 'unhealthy'
    
    def _get_warnings(self) -> List[str]:
        """Get list of system warnings."""
        warnings = []
        
        if self.total_requests == 0:
            return warnings
        
        # Check success rate
        success_rate = (
            self.successful_requests / self.total_requests * 100
        )
        if success_rate < 95:
            warnings.append(
                f"Success rate below 95%: {success_rate:.1f}%"
            )
        
        # Check average response time
        avg_time = (
            self.total_response_time / self.successful_requests
            if self.successful_requests > 0
            else 0
        )
        if avg_time > 5.0:
            warnings.append(
                f"High average response time: {avg_time:.2f}s"
            )
        
        # Check recent failures
        recent = list(self.request_history)[-10:]
        recent_failures = sum(1 for r in recent if not r['success'])
        if recent_failures >= 3:
            warnings.append(
                f"Multiple recent failures: {recent_failures}/10"
            )
        
        return warnings
    
    def get_recent_history(self, limit: int = 20) -> List[Dict]:
        """
        Get recent request history.
        
        Args:
            limit: Number of recent requests to return
            
        Returns:
            List of recent requests
        """
        history = list(self.request_history)
        return history[-limit:] if len(history) > limit else history
    
    def reset_metrics(self) -> None:
        """Reset all metrics (admin function)."""
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_response_time = 0.0
        self.rag_requests = 0
        self.basic_requests = 0
        self.request_history.clear()
        self.start_time = datetime.now()
        
        logger.warning("Performance metrics reset")


# Global instance
_monitor = None


def get_monitor() -> PerformanceMonitor:
    """Get or create global performance monitor instance."""
    global _monitor
    if _monitor is None:
        _monitor = PerformanceMonitor()
    return _monitor
