import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Camera, CheckCircle, XCircle, Target, Zap, TrendingUp, Award, Loader2, X } from "lucide-react";
import { useState, useRef, useEffect } from "react";

const ARPractice = () => {
  const [isPracticing, setIsPracticing] = useState(false);
  const [prediction, setPrediction] = useState<{
    label: string;
    confidence: number;
    all_predictions?: Record<string, number>;
  } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const intervalRef = useRef<number | null>(null);

  const API_URL = 'http://localhost:5000/api';

  const startCamera = async () => {
    try {
      setError(null);
      console.log('🎥 ========== STARTING CAMERA ==========');
      console.log('📍 Requesting camera access...');
      
      // Check if getUserMedia is supported
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.error('❌ Camera API not supported');
        setError('Camera API not supported in this browser. Please use a modern browser.');
        return;
      }
      
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { 
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user'
        }
      });
      
      console.log('✅ Camera access granted!');
      console.log('📹 Stream:', stream);
      console.log('📹 Video tracks:', stream.getVideoTracks());
      
      // Store stream first
      streamRef.current = stream;
      
      // Set isPracticing to true to render the video element
      setIsPracticing(true);
      console.log('✅ isPracticing set to true - video element should render now');
      
      // Wait for next render cycle when video element exists
      setTimeout(() => {
        const video = videoRef.current;
        
        if (!video) {
          console.error('❌ Video element not found after render!');
          setError('Failed to initialize video element');
          return;
        }
        
        console.log('✅ Video element found!');
        console.log('🔧 Setting srcObject on video element...');
        video.srcObject = stream;
        
        // Wait for video to be ready and play it
        const handleLoadedMetadata = async () => {
          console.log('✅ Video metadata loaded');
          console.log('📺 Video dimensions:', video.videoWidth, 'x', video.videoHeight);
          
          try {
            await video.play();
            console.log('✅ Video playing successfully!');
            
            // Start prediction loop after video is playing
            intervalRef.current = window.setInterval(() => {
              captureAndPredict();
            }, 1000); // Predict every second
            console.log('✅ Prediction loop started (every 1 second)');
            console.log('🎥 ========== CAMERA READY ==========');
          } catch (err) {
            console.error('❌ Error playing video:', err);
            setError('Failed to play video stream.');
          }
        };
        
        video.addEventListener('loadedmetadata', handleLoadedMetadata);
        
        // Fallback: if loadedmetadata doesn't fire quickly, try to play anyway
        setTimeout(() => {
          if (video.readyState >= 2) {
            console.log('⚡ Fallback: Video ready, attempting play...');
            handleLoadedMetadata();
          } else {
            console.log('⏳ Video readyState:', video.readyState);
          }
        }, 1000);
      }, 100); // Small delay to let React render the video element
    } catch (err: any) {
      console.error('Camera error:', err);
      if (err.name === 'NotAllowedError') {
        setError('Camera permission denied. Please allow camera access in your browser settings.');
      } else if (err.name === 'NotFoundError') {
        setError('No camera found. Please connect a camera and try again.');
      } else if (err.name === 'NotReadableError') {
        setError('Camera is already in use by another application.');
      } else {
        setError(`Failed to access camera: ${err.message}`);
      }
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    
    setIsPracticing(false);
    setPrediction(null);
  };

  const captureAndPredict = async () => {
    if (!videoRef.current || !canvasRef.current) {
      console.warn('⚠️ Video or canvas ref not available');
      return;
    }
    
    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    if (video.videoWidth === 0 || video.videoHeight === 0) {
      console.warn('⚠️ Video not ready yet');
      return;
    }
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    ctx.drawImage(video, 0, 0);
    console.log('📸 Frame captured:', canvas.width, 'x', canvas.height);
    
    // Convert canvas to base64
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    console.log('🖼️ Image converted to base64, length:', imageData.length);
    
    try {
      setIsLoading(true);
      console.log('📡 Sending to API:', API_URL + '/predict');
      
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
      });
      
      console.log('📥 Response status:', response.status);
      const result = await response.json();
      console.log('📦 Result:', result);
      
      if (result.success) {
        console.log('🎯 PREDICTION:', result.label, '(', (result.confidence * 100).toFixed(1), '% confidence)');
        setPrediction({
          label: result.label,
          confidence: result.confidence,
          all_predictions: result.all_predictions
        });
      } else {
        console.log('⚠️ No prediction:', result.error || 'Unknown error');
        setPrediction(null);
      }
    } catch (err) {
      console.error('❌ Prediction error:', err);
      setError('Failed to connect to AI model. Make sure the server is running.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  const practiceModules = [
    {
      title: "Alphabets A-Z",
      difficulty: "Beginner",
      signs: 26,
      accuracy: 92,
      color: "border-primary/50 bg-primary/5"
    },
    {
      title: "Numbers 1-10",
      difficulty: "Beginner",
      signs: 10,
      accuracy: 88,
      color: "border-secondary/50 bg-secondary/5"
    },
    {
      title: "Common Greetings",
      difficulty: "Intermediate",
      signs: 15,
      accuracy: 75,
      color: "border-accent/50 bg-accent/5"
    },
    {
      title: "Daily Conversations",
      difficulty: "Advanced",
      signs: 30,
      accuracy: 0,
      color: "border-primary-light/50 bg-primary-light/5"
    }
  ];

  const feedbackExamples = [
    { type: "correct", message: "Perfect! Your hand position is accurate.", icon: CheckCircle, color: "text-green-500" },
    { type: "tip", message: "Move your hand slightly higher for better clarity.", icon: Target, color: "text-primary" },
    { type: "incorrect", message: "Try bending your fingers more gently.", icon: XCircle, color: "text-destructive" }
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <section className="pt-32 pb-16 bg-gradient-to-b from-accent/5 to-background">
        <div className="container mx-auto px-4">
          {/* Header */}
          <div className="text-center max-w-3xl mx-auto mb-12 animate-fade-in">
            <div className="inline-block mb-4">
              <span className="px-4 py-2 rounded-full gradient-primary text-white text-sm font-medium shadow-glow">
                AI-Powered Practice Partner
              </span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Practice with
              <span className="text-gradient block mt-2">Your AR Assistant</span>
            </h1>
            <p className="text-xl text-muted-foreground">
              Get real-time feedback on your signs with our intelligent AR practice system. 
              Perfect your technique confidently from home.
            </p>
          </div>

          {/* Main Practice Section */}
          <div className="grid lg:grid-cols-3 gap-8 mb-12">
            {/* AR Camera View */}
            <Card className="lg:col-span-2 p-8 border-2 border-primary/30 bg-gradient-to-br from-primary/5 to-transparent">
              <div className="relative aspect-video bg-black rounded-xl border-2 border-border mb-6 flex items-center justify-center overflow-hidden">
                {isPracticing ? (
                  <>
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      className="w-full h-full object-cover rounded-lg"
                    />
                    <canvas ref={canvasRef} className="hidden" />
                    
                    {/* Loading Indicator */}
                    {isLoading && (
                      <div className="absolute top-4 right-4 bg-blue-600 text-white px-4 py-2 rounded-full flex items-center gap-2 shadow-lg">
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span className="text-sm font-medium">Processing...</span>
                      </div>
                    )}
                    
                    {/* AR Frame Overlay */}
                    <div className="absolute inset-4 border-2 border-primary/50 rounded-lg pointer-events-none"></div>
                    
                    {/* Prediction Display at Bottom */}
                    {prediction && (
                      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 via-black/80 to-transparent px-6 py-6 pb-8">
                        <div className="text-center">
                          <p className="text-sm text-gray-300 mb-2">Detected Sign</p>
                          <p className="text-5xl font-bold text-white mb-2">{prediction.label}</p>
                          <div className="flex items-center justify-center gap-2">
                            <div className="h-1.5 bg-gray-700 rounded-full w-32 overflow-hidden">
                              <div 
                                className="h-full bg-gradient-to-r from-green-400 to-green-500 transition-all duration-300"
                                style={{ width: `${prediction.confidence * 100}%` }}
                              />
                            </div>
                            <span className="text-sm font-semibold text-green-400">
                              {(prediction.confidence * 100).toFixed(1)}%
                            </span>
                          </div>
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="text-center">
                    <Camera className="w-20 h-20 text-primary mx-auto mb-4 animate-pulse" />
                    <p className="text-lg font-bold text-foreground mb-2">Camera View</p>
                    <p className="text-sm text-muted-foreground">Click "Start Practice" to begin</p>
                  </div>
                )}
              </div>

              <div className="flex gap-4">
                {isPracticing ? (
                  <Button 
                    className="flex-1 bg-red-600 hover:bg-red-700 text-white"
                    onClick={stopCamera}
                  >
                    <X className="w-5 h-5 mr-2" />
                    Stop Practice
                  </Button>
                ) : (
                  <Button 
                    className="flex-1 gradient-primary text-white shadow-glow hover:shadow-medium transition-smooth"
                    onClick={startCamera}
                  >
                    <Camera className="w-5 h-5 mr-2" />
                    Start Practice
                  </Button>
                )}
                <Button variant="outline" className="flex-1">
                  <Target className="w-5 h-5 mr-2" />
                  View Instructions
                </Button>
              </div>
            </Card>

            {/* Live Feedback Panel */}
            <Card className="p-6 border-border">
              <h3 className="text-xl font-bold mb-4 text-foreground flex items-center gap-2">
                <Zap className="w-5 h-5 text-primary" />
                Live Feedback
              </h3>
              
              <div className="space-y-4">
                {prediction ? (
                  <>
                    <div className="p-4 rounded-xl border-2 border-green-500/30 bg-green-500/5">
                      <div className="flex items-start gap-3">
                        <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                        <div>
                          <p className="text-sm font-bold text-foreground mb-1">Detected: {prediction.label}</p>
                          <p className="text-xs text-muted-foreground">
                            Confidence: {(prediction.confidence * 100).toFixed(1)}%
                          </p>
                        </div>
                      </div>
                    </div>
                    
                    {prediction.all_predictions && (
                      <div className="space-y-2">
                        <h4 className="text-sm font-semibold text-muted-foreground">All Predictions:</h4>
                        {Object.entries(prediction.all_predictions)
                          .sort(([, a], [, b]) => b - a)
                          .slice(0, 5)
                          .map(([label, conf]) => (
                            <div key={label} className="flex items-center justify-between text-sm">
                              <span className="text-foreground">{label}</span>
                              <div className="flex items-center gap-2">
                                <div className="w-20 h-2 bg-muted rounded-full overflow-hidden">
                                  <div
                                    className="h-full bg-primary"
                                    style={{ width: `${conf * 100}%` }}
                                  />
                                </div>
                                <span className="text-muted-foreground w-12 text-right">
                                  {(conf * 100).toFixed(0)}%
                                </span>
                              </div>
                            </div>
                          ))}
                      </div>
                    )}
                  </>
                ) : (
                  <>
                    {feedbackExamples.map((feedback, index) => {
                      const Icon = feedback.icon;
                      return (
                        <div key={index} className={`p-4 rounded-xl border-2 ${
                          feedback.type === 'correct' ? 'border-green-500/30 bg-green-500/5' :
                          feedback.type === 'tip' ? 'border-primary/30 bg-primary/5' :
                          'border-destructive/30 bg-destructive/5'
                        }`}>
                          <div className="flex items-start gap-3">
                            <Icon className={`w-5 h-5 ${feedback.color} flex-shrink-0 mt-0.5`} />
                            <p className="text-sm text-foreground">{feedback.message}</p>
                          </div>
                        </div>
                      );
                    })}
                  </>
                )}

                {error && (
                  <div className="p-4 rounded-xl border-2 border-red-500/30 bg-red-500/5">
                    <p className="text-sm text-red-700 font-semibold">{error}</p>
                  </div>
                )}
              </div>

              <div className="mt-6 p-4 bg-accent/10 rounded-xl">
                <p className="text-sm font-medium text-center text-accent">
                  {isPracticing ? 'Keep practicing for better accuracy!' : 'Start practice to get live feedback!'}
                </p>
              </div>
            </Card>
          </div>

          {/* Practice Modules */}
          <div className="mb-12">
            <h2 className="text-3xl font-bold mb-6 text-foreground flex items-center gap-2">
              <Target className="w-7 h-7 text-primary" />
              Practice Modules
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              {practiceModules.map((module, index) => (
                <Card 
                  key={index}
                  className={`p-6 border-2 ${module.color} hover:shadow-medium transition-smooth cursor-pointer animate-fade-in`}
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-2xl font-bold text-foreground mb-1">{module.title}</h3>
                      <p className="text-sm text-muted-foreground">{module.signs} signs • {module.difficulty}</p>
                    </div>
                    {module.accuracy > 0 && (
                      <div className="text-right">
                        <p className="text-2xl font-bold text-primary">{module.accuracy}%</p>
                        <p className="text-xs text-muted-foreground">Accuracy</p>
                      </div>
                    )}
                  </div>

                  {module.accuracy > 0 ? (
                    <div className="mb-4">
                      <div className="h-2 bg-muted rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-primary transition-all" 
                          style={{ width: `${module.accuracy}%` }}
                        ></div>
                      </div>
                    </div>
                  ) : (
                    <div className="mb-4 p-3 bg-muted/30 rounded-lg">
                      <p className="text-sm text-muted-foreground text-center">Not started yet</p>
                    </div>
                  )}

                  <Button className="w-full" variant={module.accuracy > 0 ? "default" : "outline"}>
                    {module.accuracy > 0 ? 'Continue Practice' : 'Start Module'}
                  </Button>
                </Card>
              ))}
            </div>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <Card className="p-6 border-border text-center">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <Zap className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-bold mb-2 text-foreground">Real-Time Analysis</h3>
              <p className="text-sm text-muted-foreground">
                Get instant feedback as you practice each sign with AI-powered recognition
              </p>
            </Card>

            <Card className="p-6 border-border text-center">
              <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-6 h-6 text-secondary" />
              </div>
              <h3 className="text-lg font-bold mb-2 text-foreground">Track Progress</h3>
              <p className="text-sm text-muted-foreground">
                Monitor your improvement with detailed accuracy scores and statistics
              </p>
            </Card>

            <Card className="p-6 border-border text-center">
              <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center mx-auto mb-4">
                <Award className="w-6 h-6 text-accent" />
              </div>
              <h3 className="text-lg font-bold mb-2 text-foreground">Earn Achievements</h3>
              <p className="text-sm text-muted-foreground">
                Unlock badges and rewards as you master different sign categories
              </p>
            </Card>
          </div>

          {/* Tips Section */}
          <Card className="p-8 border-2 border-accent/30 bg-gradient-to-br from-accent/10 to-transparent text-center">
            <h2 className="text-3xl font-bold mb-6 text-foreground">
              Pro Tips for Better Practice
            </h2>
            <div className="grid md:grid-cols-3 gap-6 text-left">
              <div>
                <h4 className="font-bold mb-2 text-foreground">Good Lighting</h4>
                <p className="text-sm text-muted-foreground">Practice in a well-lit room for better hand detection</p>
              </div>
              <div>
                <h4 className="font-bold mb-2 text-foreground">Clear Background</h4>
                <p className="text-sm text-muted-foreground">Use a plain background to help the AI focus on your hands</p>
              </div>
              <div>
                <h4 className="font-bold mb-2 text-foreground">Camera Distance</h4>
                <p className="text-sm text-muted-foreground">Position yourself 2-3 feet from the camera for optimal results</p>
              </div>
            </div>
          </Card>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default ARPractice;
