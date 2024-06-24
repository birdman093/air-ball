interface dateRanges {
    minDate: string,
    maxDate: string
}

const dateRange: dateRanges[] = 
    [{minDate: "2024-04-02", maxDate: "2024-06-17" }];

export const getAllowableDateRanges = (year: string) => {
    return dateRange;
}

export const endAirBall = "2024-06-17";
export const beginAirBall = "2024-04-02";