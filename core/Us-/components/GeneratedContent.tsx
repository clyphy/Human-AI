import React from 'react';
import Card from './Card';
import MarkdownDisplay from './MarkdownDisplay';
import { ViewOption } from '../types';
import { DocumentIcon } from './icons/DocumentIcon';
import { CodeIcon } from './icons/CodeIcon';

interface GeneratedContentProps {
  generatedContent: string;
  viewOption: ViewOption | null;
}

const GeneratedContent: React.FC<GeneratedContentProps> = ({ generatedContent, viewOption }) => {
  const title = viewOption === 'A' ? 'Generated Design Document' : 'Generated Implementation Plan';
  const icon = viewOption === 'A' ? <DocumentIcon className="w-6 h-6 text-cyan-400" /> : <CodeIcon className="w-6 h-6 text-cyan-400" />;
  
  return (
    <Card title={title} icon={icon} className="h-full" contentClassName="overflow-y-auto">
      <MarkdownDisplay content={generatedContent} />
    </Card>
  );
};

export default GeneratedContent;