import React from 'react'
import { AiOutlineArrowUp, AiOutlineArrowDown } from "react-icons/ai";
import { FaRetweet, FaHeart, FaPlay, FaCircle } from "react-icons/fa";

import styled from "@emotion/styled";



const NewEntryIcon = styled(FaCircle)`
  color: blue;
  font-size: 12px;
  /* margin-right: 8px; */
`;

const SamePosition = styled(FaCircle)`
  color: white;
  font-size: 12px;
  /* margin-right: 8px; */
`;

const UpArrowIcon = styled(AiOutlineArrowUp)`
  color: #1db954;
  font-size: 12px;
  /* margin-left: 4px; */
`;

const DownArrowIcon = styled(AiOutlineArrowDown)`
  color: #f44336;
  font-size: 12px;
  /* margin-left: 4px; */
`;

const PositionChange = ({ current, previous }) => {
    if (previous === null) {
      return (
        <p>SamePosition</p>
      )
    }
    
    let positionChange = previous - current;
  
    if (positionChange === 0) {
      return <NewEntryIcon />;
    } else if (positionChange > 0) {
      return (
        <>
          <UpArrowIcon />
          <span style={{ color: "#1db954" }}>{Math.abs(positionChange)}</span>
        </>
      );
    } else {
      return (
        <>
          <DownArrowIcon />
          <span style={{ color: "#f44336" }}>{Math.abs(positionChange)}</span>
        </>
      );
    }
  };
  

export default PositionChange