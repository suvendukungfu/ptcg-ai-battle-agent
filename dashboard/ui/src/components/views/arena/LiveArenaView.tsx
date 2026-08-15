import React from 'react';
import { LiveBattlefield } from './LiveBattlefield';

interface LiveArenaViewProps {
  onNavigateExplainer?: () => void;
}

export const LiveArenaView: React.FC<LiveArenaViewProps> = ({ onNavigateExplainer }) => {
  return (
    <div className="space-y-6">
      <LiveBattlefield onNavigateExplainer={onNavigateExplainer} />
    </div>
  );
};

export default LiveArenaView;
