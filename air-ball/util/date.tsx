export const todayDate = (maxDateString: string) => {
    // Check based on PST time for now

    // Create a new Date object for the current time in Pacific Time
    const todayUTC = new Date();
    const offset = todayUTC.getTimezoneOffset() * 60000; // Convert offset to milliseconds
    const pacificTime = new Date(todayUTC.getTime() - offset - (7 * 3600 * 1000)); // Adjust for Pacific Time (-7 hours)

    const maxDate = new Date(maxDateString);
    maxDate.setHours(0, 0, 0, 0); // Normalize maxDate to start of the day

    // If today in Pacific Time is greater than maxDate, use maxDate instead
    const effectiveDate = pacificTime > maxDate ? maxDate : pacificTime;

    return effectiveDate.getFullYear() + '-' + 
    String(effectiveDate.getMonth() + 1).padStart(2, '0') + 
    '-' + String(effectiveDate.getDate()).padStart(2, '0');
};


export const yesterdayDate = (maxDateString: string) => {
    const utcDate = new Date();
    const offset = utcDate.getTimezoneOffset() * 60000; // Convert offset to milliseconds
    // Create a Date object for Pacific Standard Time (UTC-8)
    const pstDate = new Date(utcDate.getTime() - offset - (8 * 3600 * 1000));

    // Subtract one day to get 'yesterday' based on Pacific Standard Time
    pstDate.setDate(pstDate.getDate() - 1);

    const maxDate = new Date(maxDateString);
    maxDate.setHours(0, 0, 0, 0); // Normalize maxDate to start of the day

    // If 'yesterday' in PST is greater than maxDate, use maxDate instead
    const effectiveDate = pstDate > maxDate ? maxDate : pstDate;

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