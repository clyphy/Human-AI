import React, { useState, useEffect } from 'react';

const loadingMessages = [
    "Aligning temporal vectors...",
    "Calculating GVE outcomes...",
    "Synthesizing prophetic data streams...",
    "Verifying ethical invariants...",
    "Compiling recursive fulfillment loop...",
    "Initializing generational coherence matrix..."
];

const LoadingSpinner: React.FC = () => {
    const [message, setMessage] = useState(loadingMessages[0]);

    useEffect(() => {
        let index = 0;
        const intervalId = setInterval(() => {
            index = (index + 1) % loadingMessages.length;
            setMessage(loadingMessages[index]);
        }, 2000);

        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="flex flex-col items-center justify-center space-y-4 h-full text-center">
            <div className="w-16 h-16 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-cyan-300 font-orbitron transition-opacity duration-500">{message}</p>
        </div>
    );
};

export default LoadingSpinner;
