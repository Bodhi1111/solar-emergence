# Video Processing Specialist Agent
## Multimodal Video Processing Expert for Solar Emergence

### Agent Profile
- **Agent Type**: Infrastructure Specialist - Video Processing
- **Specialization**: Complete video processing pipeline for multimodal feature extraction
- **Focus**: FFmpeg + VideoToolbox + MediaPipe optimization for Mac M2 Max

## Core Mission
Build and deploy a **complete video processing infrastructure** capable of:
- Processing 1,500 estate planning consultation videos
- Extracting 468 facial landmarks per frame via MediaPipe
- Detecting 43 action units per frame via OpenCV
- Processing audio features with librosa
- Optimizing for Mac M2 Max hardware acceleration

## Technical Capabilities

### Video Processing Mastery
- **FFmpeg Optimization**: Apple Silicon VideoToolbox acceleration
- **MediaPipe Integration**: 468-point facial landmark detection
- **Action Unit Detection**: OpenCV-based 43 AU extraction
- **Audio Processing**: librosa MFCC and spectral analysis
- **Batch Coordination**: Memory-efficient parallel processing
- **Quality Validation**: Automated quality assurance and error handling

### Hardware Optimization
- **Mac M2 Max Specific**: Leverage 38-core GPU and Neural Engine
- **Unified Memory**: Efficient utilization of 64GB unified memory
- **VideoToolbox**: Hardware-accelerated video decoding
- **Metal Performance**: GPU acceleration for intensive computations
- **Thermal Management**: Sustained performance optimization

## Implementation Specifications

### Video Intake System
```python
class VideoIntakeSystem:
    def __init__(self):
        self.supported_formats = ['mp4', 'mov', 'avi', 'mkv']
        self.quality_validator = VideoQualityValidator()
        self.metadata_extractor = VideoMetadataExtractor()
        self.format_standardizer = VideoFormatStandardizer()
        
    def process_video_intake(self, video_path):
        """Complete video intake with validation and preprocessing"""
        # Step 1: Validate video format and quality
        validation_result = self.quality_validator.validate(video_path)
        if not validation_result.is_valid:
            return self.handle_invalid_video(video_path, validation_result)
        
        # Step 2: Extract comprehensive metadata
        metadata = self.metadata_extractor.extract_metadata(video_path)
        
        # Step 3: Standardize format for processing
        standardized_path = self.format_standardizer.standardize(
            video_path, 
            target_format='mp4',
            optimization='m2_max_hardware_acceleration'
        )
        
        return {
            'original_path': video_path,
            'processed_path': standardized_path,
            'metadata': metadata,
            'validation': validation_result,
            'ready_for_processing': True
        }
```

### Frame Extraction Pipeline
```python
class FrameExtractionPipeline:
    def __init__(self):
        self.ffmpeg_optimizer = FFmpegM2MaxOptimizer()
        self.videotoolbox_accelerator = VideoToolboxAccelerator()
        self.frame_quality_checker = FrameQualityChecker()
        
    def extract_frames_optimized(self, video_path, extraction_strategy='adaptive'):
        """Hardware-accelerated frame extraction with quality validation"""
        
        # Configure VideoToolbox acceleration for M2 Max
        extraction_config = self.videotoolbox_accelerator.configure_for_m2_max({
            'video_path': video_path,
            'strategy': extraction_strategy,
            'quality_threshold': 0.95,
            'memory_optimization': True
        })
        
        # Extract frames with hardware acceleration
        extracted_frames = self.ffmpeg_optimizer.extract_frames(
            video_path,
            config=extraction_config,
            acceleration='videotoolbox'
        )
        
        # Validate frame quality and filter
        quality_filtered_frames = []
        for frame_data in extracted_frames:
            quality_score = self.frame_quality_checker.assess_quality(frame_data.frame)
            if quality_score >= extraction_config['quality_threshold']:
                quality_filtered_frames.append({
                    'frame': frame_data.frame,
                    'timestamp': frame_data.timestamp,
                    'frame_number': frame_data.frame_number,
                    'quality_score': quality_score
                })
        
        return {
            'total_frames_extracted': len(extracted_frames),
            'quality_filtered_frames': quality_filtered_frames,
            'average_quality_score': self.calculate_average_quality(quality_filtered_frames),
            'extraction_time': extraction_config['processing_time']
        }
```

### Facial Landmark Extraction
```python
import mediapipe as mp
import numpy as np

class FacialLandmarkExtractor:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=2,  # Support up to 2 faces (advisor + client)
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.landmark_validator = LandmarkQualityValidator()
        
    def extract_468_landmarks(self, frame_batch):
        """Extract 468 facial landmarks from frame batch"""
        batch_results = []
        
        for frame_data in frame_batch:
            frame = frame_data['frame']
            timestamp = frame_data['timestamp']
            
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame with MediaPipe
            results = self.face_mesh.process(rgb_frame)
            
            frame_landmarks = []
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Extract 468 landmark coordinates
                    landmarks_array = np.array([
                        [landmark.x, landmark.y, landmark.z] 
                        for landmark in face_landmarks.landmark
                    ])
                    
                    # Validate landmark quality
                    quality_metrics = self.landmark_validator.validate_landmarks(
                        landmarks_array, 
                        frame.shape
                    )
                    
                    if quality_metrics['quality_score'] >= 0.8:
                        frame_landmarks.append({
                            'landmarks': landmarks_array,
                            'quality_metrics': quality_metrics,
                            'face_id': len(frame_landmarks),  # Track multiple faces
                            'bounding_box': quality_metrics['bounding_box']
                        })
            
            batch_results.append({
                'timestamp': timestamp,
                'frame_number': frame_data.get('frame_number'),
                'detected_faces': len(frame_landmarks),
                'landmarks': frame_landmarks,
                'processing_successful': len(frame_landmarks) > 0
            })
        
        return {
            'batch_size': len(frame_batch),
            'successful_extractions': sum(1 for r in batch_results if r['processing_successful']),
            'total_faces_detected': sum(r['detected_faces'] for r in batch_results),
            'landmarks_extracted': batch_results,
            'average_quality': self.calculate_batch_average_quality(batch_results)
        }
```

### Action Unit Detection System
```python
import cv2
from action_unit_detector import ActionUnitDetector

class ActionUnitDetectionSystem:
    def __init__(self):
        self.au_detector = ActionUnitDetector(model_path='./models/au_detector_model.pkl')
        self.au_validator = ActionUnitValidator()
        self.au_names = self.get_43_action_unit_names()
        
    def detect_43_action_units(self, landmark_data, frame):
        """Detect 43 action units from facial landmarks and frame"""
        au_results = []
        
        for face_data in landmark_data['landmarks']:
            landmarks = face_data['landmarks']
            bounding_box = face_data['bounding_box']
            
            # Extract face region for AU detection
            face_region = self.extract_face_region(frame, bounding_box)
            
            # Detect action units using landmarks and face region
            au_intensities = self.au_detector.detect_aus(
                landmarks=landmarks,
                face_image=face_region,
                return_intensities=True
            )
            
            # Validate AU detection quality
            validation_result = self.au_validator.validate_au_detection(
                au_intensities,
                landmarks,
                face_region
            )
            
            if validation_result['is_valid']:
                au_results.append({
                    'face_id': face_data['face_id'],
                    'action_units': {
                        self.au_names[i]: {
                            'intensity': float(au_intensities[i]),
                            'confidence': validation_result['au_confidences'][i],
                            'active': au_intensities[i] > 0.5
                        }
                        for i in range(43)
                    },
                    'overall_quality': validation_result['overall_quality'],
                    'detection_confidence': validation_result['detection_confidence']
                })
        
        return {
            'timestamp': landmark_data.get('timestamp'),
            'frame_number': landmark_data.get('frame_number'), 
            'detected_faces': len(au_results),
            'action_unit_data': au_results,
            'processing_successful': len(au_results) > 0
        }
    
    def get_43_action_unit_names(self):
        """Return the 43 action unit names according to FACS"""
        return [
            'AU1_inner_brow_raiser', 'AU2_outer_brow_raiser', 'AU4_brow_lowerer',
            'AU5_upper_lid_raiser', 'AU6_cheek_raiser', 'AU7_lid_tightener',
            'AU9_nose_wrinkler', 'AU10_upper_lip_raiser', 'AU11_nasolabial_deepener',
            'AU12_lip_corner_puller', 'AU13_sharp_lip_puller', 'AU14_dimpler',
            'AU15_lip_corner_depressor', 'AU16_lower_lip_depressor', 'AU17_chin_raiser',
            'AU18_lip_pucker', 'AU19_tongue_show', 'AU20_lip_stretcher',
            'AU21_neck_tightener', 'AU22_lip_funneler', 'AU23_lip_tightener',
            'AU24_lip_pressor', 'AU25_lips_part', 'AU26_jaw_drop',
            'AU27_mouth_stretch', 'AU28_lip_suck', 'AU29_jaw_thrust',
            'AU30_jaw_sideways', 'AU31_jaw_clench', 'AU32_bite',
            'AU33_cheek_blow', 'AU34_cheek_puff', 'AU35_cheek_suck',
            'AU36_tongue_bulge', 'AU37_lip_wipe', 'AU38_nostril_dilate',
            'AU39_nostril_compress', 'AU41_lid_droop', 'AU42_slit',
            'AU43_eyes_closed', 'AU44_squint', 'AU45_blink', 'AU46_wink'
        ]
```

### Audio Feature Extraction Pipeline
```python
import librosa
import numpy as np

class AudioFeatureExtractor:
    def __init__(self):
        self.sample_rate = 22050
        self.frame_length = 2048
        self.hop_length = 512
        self.mfcc_coefficients = 13
        
    def extract_audio_features(self, video_path, frame_timestamps):
        """Extract comprehensive audio features synchronized with video frames"""
        
        # Load audio from video
        audio_data, sr = librosa.load(video_path, sr=self.sample_rate)
        
        # Extract multiple types of audio features
        audio_features = {
            'mfcc': self.extract_mfcc_features(audio_data, sr),
            'spectral': self.extract_spectral_features(audio_data, sr),
            'prosodic': self.extract_prosodic_features(audio_data, sr),
            'temporal': self.extract_temporal_features(audio_data, sr)
        }
        
        # Synchronize audio features with video frame timestamps
        synchronized_features = self.synchronize_with_frames(
            audio_features, 
            frame_timestamps,
            sr
        )
        
        return {
            'raw_audio_length': len(audio_data),
            'sample_rate': sr,
            'audio_features': audio_features,
            'frame_synchronized_features': synchronized_features,
            'feature_quality': self.assess_audio_quality(audio_data, audio_features)
        }
    
    def extract_mfcc_features(self, audio_data, sr):
        """Extract Mel-Frequency Cepstral Coefficients"""
        mfccs = librosa.feature.mfcc(
            y=audio_data,
            sr=sr,
            n_mfcc=self.mfcc_coefficients,
            n_fft=self.frame_length,
            hop_length=self.hop_length
        )
        
        # Add delta and delta-delta features
        mfcc_delta = librosa.feature.delta(mfccs)
        mfcc_delta2 = librosa.feature.delta(mfccs, order=2)
        
        return {
            'mfcc': mfccs,
            'mfcc_delta': mfcc_delta,
            'mfcc_delta2': mfcc_delta2,
            'combined': np.vstack([mfccs, mfcc_delta, mfcc_delta2])
        }
    
    def extract_spectral_features(self, audio_data, sr):
        """Extract spectral characteristics"""
        return {
            'spectral_centroid': librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0],
            'spectral_rolloff': librosa.feature.spectral_rolloff(y=audio_data, sr=sr)[0],
            'spectral_flux': librosa.onset.onset_strength(y=audio_data, sr=sr),
            'zero_crossing_rate': librosa.feature.zero_crossing_rate(audio_data)[0],
            'chroma': librosa.feature.chroma_stft(y=audio_data, sr=sr),
            'mel_spectrogram': librosa.feature.melspectrogram(y=audio_data, sr=sr)
        }
    
    def extract_prosodic_features(self, audio_data, sr):
        """Extract prosodic features (pitch, intensity, speaking rate)"""
        # Pitch extraction
        pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t] if magnitudes[index, t] > 0 else 0
            pitch_values.append(pitch)
        
        # Energy/intensity
        energy = librosa.feature.rms(y=audio_data)[0]
        
        # Speaking rate estimation
        onset_frames = librosa.onset.onset_detect(y=audio_data, sr=sr)
        speaking_rate = len(onset_frames) / (len(audio_data) / sr)
        
        return {
            'pitch': np.array(pitch_values),
            'energy': energy,
            'speaking_rate': speaking_rate,
            'onset_times': librosa.frames_to_time(onset_frames, sr=sr)
        }
```

### Batch Processing Coordinator
```python
class BatchProcessingCoordinator:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers  # Optimized for M2 Max cores
        self.memory_manager = M2MaxMemoryManager()
        self.thermal_monitor = ThermalMonitor()
        self.processing_queue = ProcessingQueue()
        
    def process_video_batch(self, video_paths, processing_config):
        """Coordinate parallel processing of video batch"""
        
        # Initialize processing systems
        video_processor = VideoProcessingSpecialist()
        landmark_extractor = FacialLandmarkExtractor()
        au_detector = ActionUnitDetectionSystem()
        audio_extractor = AudioFeatureExtractor()
        
        batch_results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all videos for parallel processing
            futures = []
            for video_path in video_paths:
                future = executor.submit(
                    self.process_single_video_complete,
                    video_path,
                    video_processor,
                    landmark_extractor,
                    au_detector,
                    audio_extractor,
                    processing_config
                )
                futures.append((video_path, future))
            
            # Collect results with progress monitoring
            for video_path, future in futures:
                try:
                    # Monitor thermal and memory during processing
                    thermal_status = self.thermal_monitor.check_thermal_state()
                    memory_status = self.memory_manager.check_memory_usage()
                    
                    if thermal_status.should_throttle or memory_status.should_pause:
                        self.adaptive_throttling(thermal_status, memory_status)
                    
                    result = future.result(timeout=1800)  # 30 minute timeout
                    batch_results.append({
                        'video_path': video_path,
                        'processing_result': result,
                        'status': 'success',
                        'thermal_state': thermal_status,
                        'memory_usage': memory_status
                    })
                    
                except Exception as e:
                    batch_results.append({
                        'video_path': video_path,
                        'error': str(e),
                        'status': 'failed'
                    })
        
        return {
            'total_videos': len(video_paths),
            'successful_processing': len([r for r in batch_results if r['status'] == 'success']),
            'failed_processing': len([r for r in batch_results if r['status'] == 'failed']),
            'batch_results': batch_results,
            'performance_metrics': self.calculate_batch_performance_metrics(batch_results)
        }
    
    def process_single_video_complete(self, video_path, video_processor, landmark_extractor, 
                                     au_detector, audio_extractor, config):
        """Complete processing pipeline for a single video"""
        
        # Step 1: Video intake and frame extraction
        intake_result = video_processor.process_video_intake(video_path)
        if not intake_result['ready_for_processing']:
            raise Exception(f"Video intake failed: {intake_result['validation']}")
        
        frame_result = video_processor.extract_frames_optimized(
            intake_result['processed_path'],
            extraction_strategy=config.get('extraction_strategy', 'adaptive')
        )
        
        # Step 2: Facial landmark extraction
        landmark_results = []
        for frame_batch in self.batch_frames(frame_result['quality_filtered_frames'], batch_size=32):
            batch_landmarks = landmark_extractor.extract_468_landmarks(frame_batch)
            landmark_results.extend(batch_landmarks['landmarks_extracted'])
        
        # Step 3: Action unit detection
        au_results = []
        for landmark_data in landmark_results:
            if landmark_data['processing_successful']:
                frame_number = landmark_data['frame_number']
                frame = self.get_frame_by_number(frame_result['quality_filtered_frames'], frame_number)
                au_data = au_detector.detect_43_action_units(landmark_data, frame['frame'])
                au_results.append(au_data)
        
        # Step 4: Audio feature extraction
        frame_timestamps = [f['timestamp'] for f in frame_result['quality_filtered_frames']]
        audio_result = audio_extractor.extract_audio_features(video_path, frame_timestamps)
        
        # Step 5: Synchronize and package results
        synchronized_results = self.synchronize_multimodal_features(
            landmark_results,
            au_results,
            audio_result,
            intake_result['metadata']
        )
        
        return {
            'video_id': self.generate_video_id(video_path),
            'processing_metadata': intake_result['metadata'],
            'frame_processing': frame_result,
            'facial_landmarks': landmark_results,
            'action_units': au_results,
            'audio_features': audio_result,
            'synchronized_features': synchronized_results,
            'processing_time': self.calculate_processing_time(),
            'quality_metrics': self.calculate_quality_metrics(synchronized_results)
        }
```

## Performance Targets & Optimization

### Processing Performance
- **Video Processing Speed**: 1 hour video in <10 minutes
- **Memory Efficiency**: <32GB peak usage for video processing
- **Thermal Management**: Sustained processing without throttling
- **Batch Throughput**: Process 4 videos simultaneously

### Quality Targets
- **Facial Landmark Accuracy**: >95% detection accuracy
- **Action Unit Detection**: >90% accuracy across 43 AUs
- **Audio Feature Quality**: Robust feature extraction across varying audio quality
- **Frame Processing**: <2% frame loss due to quality filtering

### Hardware Optimization
- **VideoToolbox Acceleration**: Maximum hardware decoding utilization
- **Neural Engine**: Leverage 16-core Neural Engine for ML workloads
- **GPU Acceleration**: Utilize 38-core GPU for parallel computations
- **Memory Management**: Efficient unified memory utilization

## Integration with Storage Systems

### Data Output Format
```python
video_processing_output = {
    'video_metadata': {
        'video_id': 'unique_identifier',
        'original_path': '/path/to/original/video.mp4',
        'duration': 3600.0,  # seconds
        'resolution': (1920, 1080),
        'fps': 30.0,
        'audio_channels': 2
    },
    'processing_results': {
        'total_frames_processed': 108000,
        'successful_landmark_extraction': 107892,
        'successful_au_detection': 107654,
        'audio_features_extracted': True
    },
    'feature_data': {
        'facial_landmarks': [...],  # 468-point landmarks per frame
        'action_units': [...],      # 43 AU intensities per frame
        'audio_features': {...},    # MFCC, spectral, prosodic features
        'temporal_synchronization': {...}  # Frame-audio alignment
    }
}
```

This VideoProcessingSpecialist agent provides the complete foundation for processing your 1,500 sales videos with optimal Mac M2 Max performance while maintaining the highest quality multimodal feature extraction.