// Web Speech API Hook for Speech Recognition
export const useSpeechRecognition = () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    console.warn('Speech Recognition not supported in this browser');
    return {
      isSupported: false,
      startListening: null,
      stopListening: null,
    };
  }

  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-US';

  let transcript = '';
  let isListening = false;

  const startListening = (timeout = 5000) => {
    return new Promise((resolve, reject) => {
      transcript = '';
      isListening = true;

      recognition.onstart = () => {
        console.log('Listening...');
      };

      recognition.onresult = (event) => {
        transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        console.log('Transcript:', transcript);
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        reject(new Error(event.error));
      };

      recognition.onend = () => {
        isListening = false;
        if (transcript.trim()) {
          resolve(transcript.toLowerCase());
        } else {
          reject(new Error('No speech detected'));
        }
      };

      recognition.start();

      // Auto-stop after timeout
      setTimeout(() => {
        if (isListening) {
          recognition.stop();
        }
      }, timeout);
    });
  };

  const stopListening = () => {
    if (isListening) {
      recognition.stop();
      isListening = false;
    }
  };

  return {
    isSupported: true,
    startListening,
    stopListening,
  };
};
