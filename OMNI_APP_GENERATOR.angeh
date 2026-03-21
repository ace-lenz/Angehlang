"""
Angeh Hardware Optimizer - Comprehensive Hardware Detection & Optimization
Auto-detects CPU, GPU, NPU, QPU and optimally distributes quantum dot workloads

Progressive Enhancement: S (Quantum+) → A (Workstation) → B (Desktop) → C (Mobile) → D (IoT)
"""

import platform
import os
import psutil
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Try importing hardware-specific libraries
try:
    import torch
    TORCH_AVAILABLE = True
except:
    TORCH_AVAILABLE = False

try:
    import cpuinfo
    CPUINFO_AVAILABLE = True
except:
    CPUINFO_AVAILABLE = False

# ============================================================
# HARDWARE CLASSES
# ============================================================

class HardwareClass(Enum):
    """Progressive enhancement classes"""
    S = "quantum_plus"      # Quantum+ systems
    A = "workstation"       # High-end workstations
    B = "desktop"           # Standard desktop/laptop
    C = "mobile"            # Mobile devices
    D = "iot_edge"          # IoT/Edge devices

@dataclass
class CPUProfile:
    """CPU detection and profiling"""
    cores: int
    threads: int
    architecture: str  # 'x86', 'ARM', 'RISC-V', 'Quantum'
    extensions: List[str] = field(default_factory=list)
    cache_l1: int = 0
    cache_l2: int = 0
    cache_l3: int = 0
    frequency_ghz: float = 0.0
    quantum_bits: Optional[int] = None

@dataclass
class GPUProfile:
    """GPU detection and profiling"""
    vendor: str  # 'NVIDIA', 'AMD', 'Intel', 'Apple', 'Custom'
    model: str
    vram_mb: int
    compute_units: int
    ray_tracing: bool = False
    tensor_cores: int = 0
    quantum_accelerator: bool = False
    cuda_available: bool = False
    opencl_available: bool = False

@dataclass
class NPUProfile:
    """NPU/TPU detection"""
    available: bool
    type: str  # 'GoogleTPU', 'AppleNeural', 'HuaweiNPU', 'Custom'
    ops_per_second: int = 0
    precision: str = 'FP32'  # 'INT8', 'FP16', 'BF16', 'FP32'

@dataclass
class MemoryProfile:
    """Memory and storage profiling"""
    total_ram_mb: int
    available_ram_mb: int
    speed_mhz: int = 0
    type: str = 'Unknown'  # 'DDR4', 'DDR5', 'HBM', 'Quantum'

@dataclass
class QuantumProfile:
    """Quantum co-processor (if available)"""
    qubits: int = 0
    coherence_time_us: float = 0.0
    topology: str = 'None'
    error_rate: float = 0.0

@dataclass
class CompleteHardwareProfile:
    """Complete system hardware profile"""
    cpu: CPUProfile
    gpu: Optional[GPUProfile]
    npu: NPUProfile
    memory: MemoryProfile
    quantum: QuantumProfile
    hardware_class: HardwareClass
    
    # Capabilities
    max_parallel_dots: int = 1000
    max_quantum_loops: int = 100
    real_time_fps: int = 30

# ============================================================
# HARDWARE DETECTION
# ============================================================

class HardwareOptimizer:
    """Comprehensive hardware detection and optimization"""
    
    def __init__(self):
        self.profile = self.detect_all_hardware()
        self.classify_hardware()
        self.calculate_capabilities()
    
    def detect_all_hardware(self) -> CompleteHardwareProfile:
        """Detect all available hardware"""
        cpu = self.detect_cpu()
        gpu = self.detect_gpu()
        npu = self.detect_npu()
        memory = self.detect_memory()
        quantum = self.detect_quantum()
        
        return CompleteHardwareProfile(
            cpu=cpu,
            gpu=gpu,
            npu=npu,
            memory=memory,
            quantum=quantum,
            hardware_class=HardwareClass.B  # Will be updated
        )
    
    def detect_cpu(self) -> CPUProfile:
        """Detect CPU specifications"""
        cores = psutil.cpu_count(logical=False) or 4
        threads = psutil.cpu_count(logical=True) or 8
        arch = platform.machine()
        
        # Map architecture
        if 'x86' in arch or 'AMD64' in arch:
            architecture = 'x86'
        elif 'arm' in arch.lower() or 'aarch' in arch.lower():
            architecture = 'ARM'
        elif 'riscv' in arch.lower():
            architecture = 'RISC-V'
        else:
            architecture = arch
        
        # Detect extensions
        extensions = []
        if CPUINFO_AVAILABLE:
            info = cpuinfo.get_cpu_info()
            if 'flags' in info:
                flags = info['flags']
                if 'avx2' in flags:
                    extensions.append('AVX2')
                if 'avx512' in flags or 'avx512f' in flags:
                    extensions.append('AVX-512')
                if 'neon' in flags:
                    extensions.append('NEON')
        
        # Get frequency
        try:
            freq = psutil.cpu_freq()
            frequency_ghz = freq.current / 1000.0 if freq else 0.0
        except:
            frequency_ghz = 0.0
        
        return CPUProfile(
            cores=cores,
            threads=threads,
            architecture=architecture,
            extensions=extensions,
            frequency_ghz=frequency_ghz
        )
    
    def detect_gpu(self) -> Optional[GPUProfile]:
        """Detect GPU specifications"""
        if not TORCH_AVAILABLE:
            return None
        
        if torch.cuda.is_available():
            # NVIDIA CUDA
            device_name = torch.cuda.get_device_name(0)
            vram_b = torch.cuda.get_device_properties(0).total_memory
            vram_mb = vram_b // (1024 * 1024)
            compute_capability = torch.cuda.get_device_properties(0).major
            
            # Estimate tensor cores (rough approximation)
            tensor_cores = 0
            if 'RTX' in device_name or 'A100' in device_name:
                tensor_cores = 320  # Approximate
            
            return GPUProfile(
                vendor='NVIDIA',
                model=device_name,
                vram_mb=vram_mb,
                compute_units=torch.cuda.get_device_properties(0).multi_processor_count,
                ray_tracing='RTX' in device_name,
                tensor_cores=tensor_cores,
                cuda_available=True
            )
        elif hasattr(torch, 'hip') and torch.hip.is_available():
            # AMD ROCm
            return GPUProfile(
                vendor='AMD',
                model='ROCm GPU',
                vram_mb=0,  # Would need specific detection
                compute_units=0,
                opencl_available=True
            )
        
        return None
    
    def detect_npu(self) -> NPUProfile:
        """Detect NPU/TPU"""
        # Check for Apple Neural Engine
        if platform.system() == 'Darwin' and platform.machine() == 'arm64':
            return NPUProfile(
                available=True,
                type='AppleNeural',
                ops_per_second=11_000_000_000_000,  # 11 TOPS for M1
                precision='FP16'
            )
        
        # Check for other NPUs (would need specific libraries)
        return NPUProfile(available=False, type='None')
    
    def detect_memory(self) -> MemoryProfile:
        """Detect memory specifications"""
        mem = psutil.virtual_memory()
        total_mb = mem.total // (1024 * 1024)
        available_mb = mem.available // (1024 * 1024)
        
        return MemoryProfile(
            total_ram_mb=total_mb,
            available_ram_mb=available_mb
        )
    
    def detect_quantum(self) -> QuantumProfile:
        """Detect quantum co-processor (if available)"""
        # Placeholder - would integrate with quantum hardware SDKs
        # e.g., IBM Qiskit, Google Cirq, AWS Braket
        return QuantumProfile()
    
    def classify_hardware(self):
        """Classify hardware into progressive enhancement class"""
        profile = self.profile
        
        # Class S: Quantum+
        if profile.quantum.qubits > 0:
            profile.hardware_class = HardwareClass.S
        # Class A: High-end workstation
        elif profile.cpu.cores >= 16 and profile.gpu and profile.gpu.vram_mb >= 8192:
            profile.hardware_class = HardwareClass.A
        # Class B: Desktop/Laptop
        elif profile.cpu.cores >= 4 and profile.memory.total_ram_mb >= 8192:
            profile.hardware_class = HardwareClass.B
        # Class C: Mobile
        elif profile.cpu.cores >= 2:
            profile.hardware_class = HardwareClass.C
        # Class D: IoT/Edge
        else:
            profile.hardware_class = HardwareClass.D
    
    def calculate_capabilities(self):
        """Calculate system capabilities based on hardware"""
        profile = self.profile
        hw_class = profile.hardware_class
        
        # Set capabilities based on class
        if hw_class == HardwareClass.S:
            profile.max_parallel_dots = 10_000_000  # 10 million
            profile.max_quantum_loops = 10_000
            profile.real_time_fps = 120
        elif hw_class == HardwareClass.A:
            profile.max_parallel_dots = 1_000_000  # 1 million
            profile.max_quantum_loops = 1000
            profile.real_time_fps = 60
        elif hw_class == HardwareClass.B:
            profile.max_parallel_dots = 100_000
            profile.max_quantum_loops = 100
            profile.real_time_fps = 30
        elif hw_class == HardwareClass.C:
            profile.max_parallel_dots = 10_000
            profile.max_quantum_loops = 10
            profile.real_time_fps = 30
        else:  # Class D
            profile.max_parallel_dots = 1_000
            profile.max_quantum_loops = 1
            profile.real_time_fps = 15
    
    def optimize_workload(self, dot_count: int, operation_type: str) -> Dict[str, any]:
        """Determine optimal hardware allocation for workload"""
        profile = self.profile
        
        # Classify operation by hardware affinity
        if operation_type in ['matrix', 'tensor', 'vector']:
            # GPU/NPU preferred
            if profile.gpu and profile.gpu.cuda_available:
                return {
                    'device': 'cuda',
                    'batch_size': min(dot_count, 10000),
                    'parallel_workers': profile.gpu.compute_units
                }
            elif profile.npu.available:
                return {
                    'device': 'npu',
                    'batch_size': min(dot_count, 5000),
                    'parallel_workers': 16
                }
        
        # CPU fallback or preferred for certain operations
        return {
            'device': 'cpu',
            'batch_size': min(dot_count, 1000),
            'parallel_workers': profile.cpu.threads
        }
    
    def get_summary(self) -> str:
        """Get human-readable hardware summary"""
        p = self.profile
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║          Angeh Hardware Profile - Class {p.hardware_class.value.upper()}          ║
╠══════════════════════════════════════════════════════════════╣
║ CPU:     {p.cpu.cores} cores / {p.cpu.threads} threads ({p.cpu.architecture})
║          {', '.join(p.cpu.extensions) if p.cpu.extensions else 'No SIMD extensions detected'}
║ GPU:     {p.gpu.model if p.gpu else 'None detected'}
║          {f'{p.gpu.vram_mb}MB VRAM, {p.gpu.compute_units} CUs' if p.gpu else ''}
║ NPU:     {p.npu.type if p.npu.available else 'Not available'}
║ Memory:  {p.memory.total_ram_mb}MB RAM ({p.memory.available_ram_mb}MB available)
║ Quantum: {f'{p.quantum.qubits} qubits' if p.quantum.qubits > 0 else 'Not available'}
╠══════════════════════════════════════════════════════════════╣
║ Capabilities:
║  • Max Parallel Dots:    {p.max_parallel_dots:,}
║  • Max Quantum Loops:    {p.max_quantum_loops:,}
║  • Real-time FPS:        {p.real_time_fps}
╚══════════════════════════════════════════════════════════════╝
"""
        return summary

# ============================================================
# GLOBAL INSTANCE
# ============================================================

# Create global hardware optimizer instance
hardware_optimizer = HardwareOptimizer()

if __name__ == "__main__":
    print(hardware_optimizer.get_summary())
    
    # Test workload optimization
    print("\n🔧 Workload Optimization Examples:")
    print("\n1. Matrix operations (10,000 dots):")
    print(json.dumps(hardware_optimizer.optimize_workload(10000, 'matrix'), indent=2))
    
    print("\n2. Sequential logic (1,000 dots):")
    print(json.dumps(hardware_optimizer.optimize_workload(1000, 'sequential'), indent=2))
