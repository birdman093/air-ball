import React from 'react';

interface TeamDisplayProps {
  imageUrl: string | null;
  abbreviation: string;
}

export const TeamDisplay: React.FC<TeamDisplayProps> = ({ imageUrl, abbreviation }) => {
    return (
      imageUrl ? (
        <img className="team-image" src={imageUrl} alt={abbreviation} />
      ) : (
        abbreviation
      )
    );
  }
  