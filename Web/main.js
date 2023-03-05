navigator.mediaDevices
  .getUserMedia({ video: false, audio: true })
  .then((stream) => {
    // Create and configure the audio pipeline
    const audioContext = new AudioContext();
    const analyzer = audioContext.createAnalyser();
    analyzer.fftSize = 512;
    analyzer.smoothingTimeConstant = 0.1;
    const sourceNode = audioContext.createMediaStreamSource(stream);
    sourceNode.connect(analyzer);

    // Analyze the sound
    setInterval(() => {
        // Compute the max volume level (-Infinity...0)
        const fftBins = new Float32Array(analyzer.frequencyBinCount); // Number of values manipulated for each sample
      analyzer.getFloatFrequencyData(fftBins);
        // audioPeakDB varies from -Infinity up to 0
      const audioPeakDB = Math.max(...fftBins);

        // Compute a wave (0...)
        const frequencyRangeData = new Uint8Array(analyzer.frequencyBinCount);
      analyzer.getByteFrequencyData(frequencyRangeData);
      const sum = frequencyRangeData.reduce((p, c) => p + c, 0);
        // audioMeter varies from 0 to 10
      const audioMeter = Math.sqrt(sum / frequencyRangeData.length);

      console.log(audioMeter)
    }, 100);
  })
  .catch((err) => {
    console.error(`you got an error: ${err}`);
  });
