export function teamNameConversion (teamName: string): string {
    const teamMap: { [key: string]: string } = {
      "Los Angeles Clippers": "LA Clippers",
    };
    return teamMap[teamName] || teamName;
  }