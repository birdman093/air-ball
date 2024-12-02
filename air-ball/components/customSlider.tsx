import Slider from '@mui/material/Slider';
import { styled } from '@mui/system';

export const CustomSlider = styled(Slider)`
  width: 100%;
  position: relative;
  margin: 20px 0; /* Adjust margin if needed */
  padding: 0; /* Remove extra padding around the slider */

  & .MuiSlider-root {
    display: none; /* Hide the slider */
  }

  /* Optional: If specific elements need explicit hiding */
  & .MuiSlider-track,
  & .MuiSlider-thumb {
    display: none; /* Explicitly hide all slider components */
  }

  & .MuiSlider-mark {
    width: 36px; /* Adjust image size */
    height: 36px;
    border-radius: 50%;
    background-size: cover;
    background-position: center;
    position: absolute;
    top: 50%; /* Align vertically over the slider */
    transform: translate(-50%, -50%); /* Center on the mark position */
    background-color: #ccc;
  }

  & .MuiSlider-track {
    position: relative;
    height: 8px; /* Adjust height of the slider track */
    background-color: #ccc; /* Blue slider color */
  }

  & .MuiSlider-rail {
    height: 8px; /* Same as track height for consistency */
    background-color: #ccc; /* Grey color for inactive part */
  }
`;