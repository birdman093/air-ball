export const todayDate = (maxDateString: string) => {
    const today = new Date();
    const maxDate = new Date(maxDateString);
    
    // If today is greater than maxDate, use maxDate instead
    const effectiveDate = today > maxDate ? maxDate : today;

    return effectiveDate.getFullYear() + '-' + 
    String(effectiveDate.getMonth() + 1).padStart(2, '0') + 
    '-' + String(effectiveDate.getDate()).padStart(2, '0');
};

export const yesterdayDate = (maxDateString: string) => {
    const today = new Date();
    today.setDate(today.getDate() - 1);
    const maxDate = new Date(maxDateString);
    
    // If today is greater than maxDate, use maxDate instead
    const effectiveDate = today > maxDate ? maxDate : today;

    return effectiveDate.getFullYear() + '-' + 
    String(effectiveDate.getMonth() + 1).padStart(2, '0') + 
    '-' + String(effectiveDate.getDate()).padStart(2, '0');
};


export const nbaGamesNextDayDate = (today: string) => {
    const date = new Date(today);
    date.setDate(date.getDate() + 1);
    return date.toISOString().split('T')[0];
};

export const convertUTCtoPSTString = (utcString: string): string => {
  // Create a Date object from the UTC string
  const utcDate = new Date(utcString);
  const pstDateString = utcDate.toLocaleString("en-US", {
      timeZone: "America/Los_Angeles",
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
  });
  const [month, day, year] = pstDateString.split('/');
  return `${year}-${month}-${day}`;
};


export const isDateToday = (gameDate: string) => {
    // Get today's date
    const today = new Date();
  
    // Convert today to string format "YYYY-MM-DD"
    const todayStr = today.toISOString().split('T')[0];
  
    // Compare the input date string to today's date string
    return gameDate === todayStr;
  };