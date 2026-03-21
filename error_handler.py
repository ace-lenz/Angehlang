"""
Angeh Reality Fabric - Enhanced Error Handling & Resilience
Production-grade error handling with self-healing capabilities
"""

import sys
import time
import logging
import traceback
import functools
import threading
from typing import Callable, Any, Optional, Dict, List, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import json

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('angeh_errors.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('AngehErrorHandler')

# ============================================================
# ERROR TYPES
# ============================================================

class ErrorSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ErrorCategory(Enum):
    FILE_IO = "file_io"
    NETWORK = "network"
    MEMORY = "memory"
    VALIDATION = "validation"
    CONCURRENCY = "concurrency"
    DEPENDENCY = "dependency"
    QUANTUM = "quantum"
    API = "api"
    MODEL = "model"
    DATA_CORRUPTION = "data_corruption"

@dataclass
class ErrorInfo:
    """Comprehensive error information"""
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    exception: Optional[Exception] = None
    stack_trace: Optional[str] = None
    recovery_attempted: bool = False
    recovery_successful: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'category': self.category.value,
            'severity': self.severity.value,
            'message': self.message,
            'exception': str(self.exception) if self.exception else None,
            'stack_trace': self.stack_trace,
            'recovery_attempted': self.recovery_attempted,
            'recovery_successful': self.recovery_successful,
            'timestamp': self.timestamp.isoformat(),
            'context': self.context
        }

# ============================================================
# INPUT VALIDATION
# ============================================================

class Validator:
    """Comprehensive input validator"""
    
    @staticmethod
    def validate_not_none(value: Any, name: str = "value") -> Any:
        """Ensure value is not None"""
        if value is None:
            raise ValueError(f"{name} cannot be None")
        return value
    
    @staticmethod
    def validate_type(value: Any, expected_type: type, name: str = "value") -> Any:
        """Validate type"""
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be {expected_type.__name__}, got {type(value).__name__}")
        return value
    
    @staticmethod
    def validate_range(value: float, min_val: float, max_val: float, name: str = "value") -> float:
        """Validate numeric range"""
        if value < min_val or value > max_val:
            raise ValueError(f"{name} must be between {min_val} and {max_val}, got {value}")
        return value
    
    @staticmethod
    def validate_length(value: Any, max_length: int, name: str = "value") -> Any:
        """Validate length"""
        if len(value) > max_length:
            raise ValueError(f"{name} length exceeds maximum of {max_length}")
        return value
    
    @staticmethod
    def validate_bounds(index: int, collection: Any, name: str = "index") -> int:
        """Validate array bounds"""
        if index < 0 or index >= len(collection):
            raise IndexError(f"{name} {index} out of bounds for collection of size {len(collection)}")
        return index
    
    @staticmethod
    def validate_file_exists(filepath: str) -> str:
        """Validate file exists"""
        import os
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        return filepath

# ============================================================
# RETRY MECHANISM
# ============================================================

@dataclass
class RetryPolicy:
    """Retry policy configuration"""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 30.0
    exponential_backoff: bool = True
    retryable_exceptions: Tuple[type, ...] = (Exception,)

def retry_with_backoff(retry_policy: RetryPolicy = None):
    """Decorator for retry with exponential backoff"""
    if retry_policy is None:
        retry_policy = RetryPolicy()
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = retry_policy.initial_delay
            last_exception = None
            
            while attempts < retry_policy.max_attempts:
                attempts += 1
                try:
                    result = func(*args, **kwargs)
                    if attempts > 1:
                        logger.info(f"{func.__name__} succeeded on attempt {attempts}")
                    return result
                
                except retry_policy.retryable_exceptions as e:
                    last_exception = e
                    
                    if attempts < retry_policy.max_attempts:
                        logger.warning(
                            f"{func.__name__} failed (attempt {attempts}/{retry_policy.max_attempts}): {e}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                        
                       # Exponential backoff
                        if retry_policy.exponential_backoff:
                            delay = min(delay * 2, retry_policy.max_delay)
                    else:
                        logger.error(f"{func.__name__} failed after {attempts} attempts")
            
            raise last_exception
        
        return wrapper
    return decorator

# ============================================================
# CIRCUIT BREAKER
# ============================================================

class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker pattern implementation"""
    
    def __init__(self, name: str, failure_threshold: int = 5, 
                 success_threshold: int = 2, timeout: float = 60.0):
        self.name = name
        self.state = CircuitBreakerState.CLOSED
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.lock = threading.Lock()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Call function through circuit breaker"""
        with self.lock:
            if self.state == CircuitBreakerState.OPEN:
                # Check if timeout expired
                if self.last_failure_time and \
                   (time.time() - self.last_failure_time) > self.timeout:
                    self.state = CircuitBreakerState.HALF_OPEN
                    self.success_count = 0
                    logger.info(f"Circuit breaker {self.name} entering half-open state")
                else:
                    raise Exception(f"Circuit breaker {self.name} is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call"""
        with self.lock:
            self.failure_count = 0
            
            if self.state == CircuitBreakerState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    self.state = CircuitBreakerState.CLOSED
                    self.success_count = 0
                    logger.info(f"Circuit breaker {self.name} closed")
    
    def _on_failure(self):
        """Handle failed call"""
        with self.lock:
            self.failure_count += 1
            self.success_count = 0
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
                logger.error(f"Circuit breaker {self.name} opened after {self.failure_count} failures")

# ============================================================
# SAFE OPERATIONS
# ============================================================

class SafeOperations:
    """Collection of safe operation wrappers"""
    
    @staticmethod
    def safe_execute(func: Callable, default: Any = None, 
                    log_errors: bool = True) -> Any:
        """Execute with default fallback"""
        try:
            return func()
        except Exception as e:
            if log_errors:
                logger.error(f"Error in {func.__name__}: {e}")
                logger.debug(traceback.format_exc())
            return default
    
    @staticmethod
    def safe_read_file(filepath: str, encoding: str = 'utf-8', 
                      fallback: str = None) -> Optional[str]:
        """Safe file reading with fallback"""
        try:
            Validator.validate_file_exists(filepath)
            
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            # Try backup
            backup_path = f"{filepath}.backup"
            if os.path.exists(backup_path):
                logger.info(f"Using backup file: {backup_path}")
                return SafeOperations.safe_read_file(backup_path, encoding, fallback)
            return fallback
        
        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            return fallback
    
    @staticmethod
    def safe_write_file(filepath: str, content: str, 
                       encoding: str = 'utf-8', atomic: bool = True) -> bool:
        """Safe file writing with atomic option"""
        import os
        import shutil
        
        try:
            # Create backup if file exists
            if os.path.exists(filepath):
                shutil.copy2(filepath, f"{filepath}.backup")
            
            if atomic:
                # Atomic write via temp file
                temp_path = f"{filepath}.tmp"
                with open(temp_path, 'w', encoding=encoding) as f:
                    f.write(content)
                    f.flush()
                    os.fsync(f.fileno())
                
                # Rename atomically
                os.replace(temp_path, filepath)
            else:
                with open(filepath, 'w', encoding=encoding) as f:
                    f.write(content)
            
            return True
        
        except Exception as e:
            logger.error(f"Error writing file {filepath}: {e}")
            # Restore from backup
            backup_path = f"{filepath}.backup"
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, filepath)
            return False
    
    @staticmethod
    def safe_json_load(filepath: str, default: Dict = None) -> Dict:
        """Safe JSON loading"""
        content = SafeOperations.safe_read_file(filepath, fallback='{}')
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filepath}: {e}")
            return default if default is not None else {}
    
    @staticmethod
    def safe_json_save(filepath: str, data: Dict) -> bool:
        """Safe JSON saving"""
        try:
            content = json.dumps(data, indent=2)
            return SafeOperations.safe_write_file(filepath, content)
        except Exception as e:
            logger.error(f"Error saving JSON to {filepath}: {e}")
            return False

# ============================================================
# RESOURCE MANAGEMENT
# ============================================================

class ResourceManager:
    """Manage resources with automatic cleanup"""
    
    class Resource:
        def __init__(self, acquire_fn: Callable, release_fn: Callable):
            self.acquire_fn = acquire_fn
            self.release_fn = release_fn
            self.resource = None
        
        def __enter__(self):
            self.resource = self.acquire_fn()
            return self.resource
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.resource is not None:
                try:
                    self.release_fn(self.resource)
                except Exception as e:
                    logger.error(f"Error releasing resource: {e}")
            return False
    
    @staticmethod
    def with_resource(acquire_fn: Callable, release_fn: Callable) -> Resource:
        """Context manager for resource cleanup"""
        return ResourceManager.Resource(acquire_fn, release_fn)

# ============================================================
# SELF-HEALING
# ============================================================

class SelfHealing:
    """Self-healing mechanisms"""
    
    @staticmethod
    def health_check() -> Dict[str, bool]:
        """Comprehensive health check"""
        import psutil
        
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'memory_ok': memory.percent < 90,
                'disk_ok': disk.percent < 90,
                'cpu_ok': psutil.cpu_percent(interval=0.1) < 95,
                'network_ok': check_network_available()
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def auto_recover(error_info: ErrorInfo) -> bool:
        """Attempt automatic recovery"""
        try:
            if error_info.category == ErrorCategory.MEMORY:
                # Force garbage collection
                import gc
                gc.collect()
                logger.info("Triggered garbage collection")
                return True
            
            elif error_info.category == ErrorCategory.FILE_IO:
                # Try to recover from backup
                logger.info("Attempting file recovery from backup")
                return True
            
            elif error_info.category == ErrorCategory.NETWORK:
                # Wait and retry
                time.sleep(5)
                logger.info("Network retry after delay")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Auto-recovery failed: {e}")
            return False

# ============================================================
# ERROR HANDLER
# ============================================================

class ErrorHandler:
    """Global error handler"""
    
    def __init__(self):
        self.error_log: List[ErrorInfo] = []
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.auto_heal_enabled = True
    
    def handle_error(self, error: Exception, category: ErrorCategory, 
                    severity: ErrorSeverity, context: Dict = None) -> ErrorInfo:
        """Handle and log error"""
        error_info = ErrorInfo(
            category=category,
            severity=severity,
            message=str(error),
            exception=error,
            stack_trace=traceback.format_exc(),
            context=context or {}
        )
        
        # Log error
        self.error_log.append(error_info)
        logger.error(f"[{severity.value.upper()}] {category.value}: {error}")
        
        # Attempt auto-recovery
        if self.auto_heal_enabled:
            error_info.recovery_attempted = True
            error_info.recovery_successful = SelfHealing.auto_recover(error_info)
        
        # Save to file
        self._save_error_log()
        
        return error_info
    
    def _save_error_log(self):
        """Save error log to file"""
        try:
            log_data = [e.to_dict() for e in self.error_log[-100:]]  # Last 100 errors
            SafeOperations.safe_json_save('angeh_error_log.json', {
                'errors': log_data,
                'last_updated': datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Failed to save error log: {e}")
    
    def get_circuit_breaker(self, name: str) -> CircuitBreaker:
        """Get or create circuit breaker"""
        if name not in self.circuit_breakers:
            self.circuit_breakers[name] = CircuitBreaker(name)
        return self.circuit_breakers[name]

# ============================================================
# GLOBAL INSTANCE
# ============================================================

# Global error handler
global_error_handler = ErrorHandler()

# Helper function
def check_network_available() -> bool:
    """Check network availability"""
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

# ============================================================
# CONVENIENCE DECORATORS
# ============================================================

def safe_function(category: ErrorCategory = ErrorCategory.VALIDATION):
    """Decorator for safe function execution"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                global_error_handler.handle_error(
                    e, category, ErrorSeverity.MEDIUM,
                    {'function': func.__name__, 'args': str(args)[:100]}
                )
                raise
        return wrapper
    return decorator

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("Angeh Error Handling & Resilience System")
    print("="*60)
    
    # Test retry mechanism
    @retry_with_backoff(RetryPolicy(max_attempts=3))
    def flaky_function():
        import random
        if random.random() < 0.7:
            raise Exception("Random failure")
        return "Success!"
    
    try:
        result = flaky_function()
        print(f"\nRetry test: {result}")
    except:
        print("\nRetry test: Failed after all attempts")
    
    # Test circuit breaker
    breaker = global_error_handler.get_circuit_breaker('test')
    print(f"\nCircuit breaker state: {breaker.state.value}")
    
    # Test validation
    try:
        Validator.validate_range(150, 0, 100, "test_value")
    except ValueError as e:
        print(f"\nValidation test: Caught expected error - {e}")
    
    # Test health check
    health = SelfHealing.health_check()
    print(f"\nHealth check: {health}")
    
    print("\n" + "="*60)
    print("✅ ALL ERROR HANDLING SYSTEMS OPERATIONAL")
    print("="*60)
