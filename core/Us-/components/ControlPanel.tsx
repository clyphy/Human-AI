import React from 'react';
import { ViewOption, PXNProject } from '../types';
import Card from './Card';
import { INITIAL_SUMMARY } from '../constants';
import { DocumentIcon } from './icons/DocumentIcon';
import { CodeIcon } from './icons/CodeIcon';
import { NexusIcon } from './icons/NexusIcon';
import MarkdownDisplay from './MarkdownDisplay';

interface ControlPanelProps {
  onGenerate: (option: ViewOption) => void;
  isLoading: boolean;
  projects: PXNProject[];
  selectedProject: PXNProject;
  onSelectProject: (projectId: string) => void;
}

const ControlPanel: React.FC<ControlPanelProps> = ({ onGenerate, isLoading, projects, selectedProject, onSelectProject }) => {
  return (
    <Card 
        title="Core Mechanism Mandate" 
        icon={<div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>}
        className="h-full"
    >
      <div className="flex flex-col h-full">
        <div className="flex-grow overflow-y-auto pr-2 text-sm text-gray-400 leading-relaxed">
            <MarkdownDisplay content={INITIAL_SUMMARY} />
        </div>
        
        <div className="flex-shrink-0 border-t border-cyan-500/20 pt-6 mt-6 space-y-6">
            <div>
              <h3 className="text-md font-semibold text-cyan-400 mb-3 flex items-center gap-2">
                <NexusIcon className="w-5 h-5" />
                Select Project
              </h3>
              <select
                value={selectedProject?.id}
                onChange={(e) => onSelectProject(e.target.value)}
                disabled={isLoading}
                className="w-full bg-gray-800 border border-cyan-700/50 rounded-lg p-3 text-cyan-300 focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all"
              >
                {projects.map(project => (
                  <option key={project.id} value={project.id}>
                    {project.id}. {project.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <h3 className="text-md font-semibold text-cyan-400 mb-4">Generate Actionable Output</h3>
              <div className="flex flex-col sm:flex-row lg:flex-col gap-4">
                  <button
                      onClick={() => onGenerate('A')}
                      disabled={isLoading}
                      className="flex-1 w-full flex items-center justify-center gap-3 px-4 py-3 bg-gray-800 text-cyan-300 rounded-lg border border-cyan-700/50 hover:bg-cyan-900/50 hover:border-cyan-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed group"
                  >
                      <DocumentIcon className="w-5 h-5 text-cyan-500 group-hover:text-cyan-300 transition-colors" />
                      <span className="font-semibold">Design Document</span>
                  </button>
                  <button
                      onClick={() => onGenerate('B')}
                      disabled={isLoading}
                      className="flex-1 w-full flex items-center justify-center gap-3 px-4 py-3 bg-gray-800 text-cyan-300 rounded-lg border border-cyan-700/50 hover:bg-cyan-900/50 hover:border-cyan-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed group"
                  >
                      <CodeIcon className="w-5 h-5 text-cyan-500 group-hover:text-cyan-300 transition-colors" />
                      <span className="font-semibold">Implementation Plan</span>
                  </button>
              </div>
            </div>
        </div>
      </div>
    </Card>
  );
};

export default ControlPanel;