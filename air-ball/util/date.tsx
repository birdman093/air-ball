import { endAirBall } from "./dateRanges";

const SERVER_RUN_TIME = -10; // UTC+0 10am || UTC-10

const createCurrentDateUTCPlus10 = () => {
    const epochTime = Math.floor(new Date().getTime()/1000.0)
    const date = new Date(epochTime * 1000);
    const utcPlus10Offset = SERVER_RUN_TIME * 60;
    const currentOffset = date.getTimezoneOffset();
    const totalOffset = utcPlus10Offset - currentOffset;
    const offsetInMilliseconds = totalOffset * 60 * 1000;
    const utcPlus10Date = new Date(date.getTime() + offsetInMilliseconds);
    return utcPlus10Date;
}

const getDateInUTCPlus10 = (year: number, month: number, day: number) => {
    const date = new Date(Date.UTC(year, month - 1, day, 0, 0, 0));

    // Get the UTC+10 offset in milliseconds (10 hours * 60 minutes/hour 
    // * 60 seconds/minute * 1000 milliseconds/second)
    const utcPlus10Offset = SERVER_RUN_TIME * 60 * 60 * 1000;
    const utcDate = new Date(date.getTime() - utcPlus10Offset);
    return utcDate;
}


export const todayDate = () => {
    const todayDate = createCurrentDateUTCPlus10();
    todayDate.setHours(0, 0, 0, 0);

    const [year, month, day] = endAirBall.split("-")
    const maxDate = getDateInUTCPlus10(Number(year), Number(month), Number(day));
    maxDate.setHours(0, 0, 0, 0);

    const effectiveDate = todayDate > maxDate ? maxDate : todayDate;

    console.log(effectiveDate);

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
    maxDate.setDate(maxDate.getDate() - 1);

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