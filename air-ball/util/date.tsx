export const todayDate = (maxDateString: string) => {
    // Check based on PST time for now

    // Create a new Date object for the current time in Pacific Time
    const todayPST = new Date().toLocaleString("en-US", { timeZone: "America/Los_Angeles" });
    const todayDate = new Date(todayPST);

    // Normalize todayDate to start of the day in PST
    todayDate.setHours(0, 0, 0, 0);

    const maxDate = new Date(maxDateString);
    maxDate.setHours(0, 0, 0, 0); // Normalize maxDate to start of the day

    // If today in Pacific Time is greater than maxDate, use maxDate instead
    const effectiveDate = todayDate > maxDate ? maxDate : todayDate;

    return effectiveDate.toISOString().split('T')[0]; // Returns date in YYYY-MM-DD format
};


export const yesterdayDate = (maxDateString: string) => {
    // Create a new Date object for 'yesterday' in Pacific Time
    const todayPST = new Date().toLocaleString("en-US", { timeZone: "America/Los_Angeles" });
    const todayDate = new Date(todayPST);

    // Subtract one day to get 'yesterday'
    todayDate.setDate(todayDate.getDate() - 1);
    todayDate.setHours(0, 0, 0, 0); // Normalize 'yesterday' to start of the day in PST

    const maxDate = new Date(maxDateString);
    maxDate.setHours(0, 0, 0, 0); // Normalize maxDate to start of the day

    // If 'yesterday' in Pacific Time is greater than maxDate, use maxDate instead
    const effectiveDate = todayDate > maxDate ? maxDate : todayDate;

    return effectiveDate.toISOString().split('T')[0];
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