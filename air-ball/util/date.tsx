export const todayDate = () => {
    const today = new Date()
    return  today.getFullYear() + '-' + 
    String(today.getMonth() + 1).padStart(2, '0') + 
    '-' + String(today.getDate()).padStart(2, '0');
}

export const nbaAPIDate = (today: string) => {
    // Parse the date string
    const dateParts = today.split('-');
    const year = parseInt(dateParts[0], 10);
    const month = parseInt(dateParts[1], 10) - 1; // Month is 0-indexed in JavaScript Date
    const day = parseInt(dateParts[2], 10);

    // Create a new Date object and add one day
    const date = new Date(year, month, day);
    date.setDate(date.getDate() + 1);

    // Format the new date back into a string
    const nextDayString = date.getFullYear() + '-' + 
                          String(date.getMonth() + 1).padStart(2, '0') + '-' + 
                          String(date.getDate()).padStart(2, '0');

    return nextDayString;
}