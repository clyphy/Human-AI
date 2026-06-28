import React, { useState } from 'react';

// Helper to render inline code snippets
const renderWithInlineFormatting = (text: string): React.ReactNode => {
    const parts = text.split(/(`[^`]+`)/g);
    return parts.map((part, i) => {
        if (part.startsWith('`') && part.endsWith('`')) {
            return <code key={i} className="text-pink-400 bg-gray-800 p-1 rounded-md mx-1 font-mono text-sm">{part.slice(1, -1)}</code>;
        }
        return part;
    });
};

// A self-contained component for rendering code blocks with a copy button
const CodeBlock: React.FC<{ code: string }> = ({ code }) => {
    const [isCopied, setIsCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(code).then(() => {
            setIsCopied(true);
            setTimeout(() => setIsCopied(false), 2000);
        });
    };

    return (
        <div className="relative my-4 group">
            <button
                onClick={handleCopy}
                className="absolute top-3 right-3 p-1.5 bg-gray-800/80 rounded-md text-gray-400 hover:text-cyan-300 hover:bg-gray-700/80 transition-all opacity-0 group-hover:opacity-100 duration-200"
                aria-label="Copy code"
            >
                {isCopied ? (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                )}
            </button>
            <pre className="bg-gray-900/70 border border-cyan-800/50 p-4 rounded-md overflow-x-auto text-sm">
                <code>{code}</code>
            </pre>
        </div>
    );
};

const MarkdownDisplay: React.FC<{ content: string; className?: string }> = ({ content, className }) => {
    const blocks = content.split('\n\n');

    return (
        <div className={`prose prose-invert prose-sm md:prose-base max-w-none text-gray-300 prose-headings:text-cyan-400 prose-strong:text-cyan-300 prose-code:text-pink-400 prose-code:bg-gray-800 prose-code:p-1 prose-code:rounded-md prose-pre:bg-gray-800/50 prose-pre:border prose-pre:border-cyan-800/50 ${className}`}>
            {blocks.map((block, index) => {
                const trimmedBlock = block.trim();
                if (!trimmedBlock) return null;

                // Headers
                if (trimmedBlock.match(/^(#+\s|(\d+\.)+\d*\s).+/)) {
                    return <h2 key={index} className="font-orbitron !mt-6 !mb-3">{trimmedBlock.replace(/^#+\s*/, '')}</h2>;
                }

                if (trimmedBlock.startsWith('💡') || trimmedBlock.startsWith('📐')) {
                    return <h3 key={index} className="font-orbitron text-lg text-cyan-300 !mt-6 !mb-3">{trimmedBlock}</h3>
                }

                // Code blocks
                if (trimmedBlock.startsWith('```')) {
                    const code = trimmedBlock.replace(/```(\w+)?\n?|```/g, '').trim();
                    return <CodeBlock key={index} code={code} />;
                }

                const lines = trimmedBlock.split('\n');
                
                // Blockquote
                if (lines.every(line => line.trim().startsWith('>'))) {
                    const quoteContent = lines.map(line => line.trim().substring(1).trim()).join('\n');
                     return (
                        <blockquote key={index} className="border-l-4 border-cyan-700/50 pl-4 my-4 text-gray-400 italic">
                            <p className="whitespace-pre-wrap">{renderWithInlineFormatting(quoteContent)}</p>
                        </blockquote>
                    );
                }

                // List
                if (lines.every(line => line.trim().startsWith('* '))) {
                    return (
                        <ul key={index} className="list-disc list-inside space-y-1 my-4 pl-4">
                            {lines.map((item, i) => <li key={i}>{renderWithInlineFormatting(item.trim().substring(2))}</li>)}
                        </ul>
                    );
                }

                // Table
                if (lines.length > 1 && lines.every(line => line.trim().startsWith('|'))) {
                    if (!lines[1].includes('---')) return <p key={index} className="whitespace-pre-wrap">{renderWithInlineFormatting(trimmedBlock)}</p>;
                    
                    const headers = lines[0].split('|').map(h => h.trim()).slice(1, -1);
                    const rows = lines.slice(2).map(row => row.split('|').map(c => c.trim()).slice(1, -1));
                    return (
                        <table key={index} className="w-full my-4 border-collapse border border-cyan-800/50">
                            <thead>
                                <tr className="bg-gray-900/50">
                                    {headers.map((header, hIndex) => <th key={hIndex} className="border border-cyan-800/50 p-2 text-cyan-400 text-left font-semibold">{header}</th>)}
                                </tr>
                            </thead>
                            <tbody>
                                {rows.map((row, rIndex) => (
                                    <tr key={rIndex} className="bg-gray-800/20 hover:bg-gray-800/60">
                                        {row.map((cell, cIndex) => <td key={cIndex} className="border border-cyan-800/50 p-2">{renderWithInlineFormatting(cell)}</td>)}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    );
                }
                
                // Paragraph
                return <p key={index} className="leading-relaxed my-4 whitespace-pre-wrap">{renderWithInlineFormatting(trimmedBlock)}</p>;
            })}
        </div>
    );
};

export default MarkdownDisplay;
