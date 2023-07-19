import React, { useState } from "react";
import { songsData } from "../../data/songs";
import {
  AiFillPlayCircle,
  AiOutlineArrowUp,
  AiOutlineArrowDown,
} from "react-icons/ai";
import { FaRetweet, FaHeart, FaPlay } from "react-icons/fa";
import { GiNewBorn } from "react-icons/gi";
import { orderBy } from "lodash";
import styled from "@emotion/styled";
import {
  TableContainer,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Select,
  MenuItem,
} from "@material-ui/core";

const PositionCell = styled(TableCell)`
  /* display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center; */
  color: #b3b3b3;
`;

const SongTitleCell = styled(TableCell)`
  font-weight: bold;
  color: #fff;
`;

const TableContainerStyled = styled(TableContainer)`
  background-color: #282828;
  margin-top: 20px;
  border-radius: 15px;
`;

const NewEntryIcon = styled(GiNewBorn)`
  color: #1db954;
  font-size: 24px;
  margin-right: 8px;
`;

const UpArrowIcon = styled(AiOutlineArrowUp)`
  color: #1db954;
  font-size: 18px;
  margin-left: 4px;
`;

const DownArrowIcon = styled(AiOutlineArrowDown)`
  color: #f44336;
  font-size: 18px;
  margin-left: 4px;
`;
const LikeIcon = styled(FaHeart)`
  color: #ff5500;
  font-size: 16px;
  margin-right: 4px;
`;

const RepostIcon = styled(FaRetweet)`
  color: #ff5500;
  font-size: 16px;
  margin-right: 4px;
`;

const PlayIcon = styled(FaPlay)`
  color: #ff5500;
  font-size: 16px;
  margin-right: 4px;
`;
const StyledTableCell = styled(TableCell)`
  color: #b3b3b3;
`;

const StyledTableHeadCell = styled(TableCell)`
  color: #b3b3b3;
  font-weight: bold;
`;

const SongTableContainer = styled.div`
  background-color: #121212;
  min-height: 100vh;
  padding: 20px;
`;

const ChartTitle = styled.h1`
  text-align: center;
  color: #fff;
`;

const FilterContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
`;

const FilterLabel = styled.span`
  color: #fff;
  margin-right: 8px;
`;

const FilterSelect = styled(Select)`
  color: #fff;
  margin-right: 16px;
`;

const PlayButton = styled.button`
  background-color: transparent;
  border: none;
  cursor: pointer;
`;

const IframeContainer = styled.div`
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const SongTable = () => {
  const [filter, setFilter] = useState("position");
  const [selectedGenre, setSelectedGenre] = useState("hardstyle");
  const [selectedDate, setSelectedDate] = useState("all");
  let filteredSongs;

  switch (filter) {
    case "mostPlayed":
      filteredSongs = orderBy(songsData, ["plays_number"], ["desc"]);
      break;
    case "newlyAdded":
      filteredSongs = orderBy(songsData, ["date_added"], ["desc"]);
      break;
    default:
      filteredSongs = orderBy(songsData, ["current_position"], ["asc"]);
  }

  if (selectedGenre !== "all") {
    filteredSongs = filteredSongs.filter((song) => song.tags === selectedGenre);
  }

  if (selectedDate !== "all") {
    filteredSongs = filteredSongs.filter((song) => {
      const songDate = new Date(song.date_added);
      const filterDate = new Date(selectedDate);
      return songDate.toDateString() === filterDate.toDateString();
    });
  }

  const handleFilterChange = (event) => {
    setFilter(event.target.value);
  };

  const handleGenreChange = (event) => {
    setSelectedGenre(event.target.value);
  };

  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
  };

  const handlePlayButtonClick = (song) => {
    console.log("Playing:", song.title);
    const playerUrl = `https://w.soundcloud.com/player/?url=${encodeURIComponent(
      song.url
    )}&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true`;
    const iframe = document.createElement("iframe");
    iframe.setAttribute("src", playerUrl);
    iframe.setAttribute("width", "100%");
    iframe.setAttribute("height", "300");
    iframe.setAttribute("frameborder", "no");
    iframe.setAttribute("scrolling", "no");
    iframe.setAttribute("title", "SoundCloud Player");
    document.getElementById("player-container").innerHTML = "";
    document.getElementById("player-container").appendChild(iframe);
  };

  const getSoundCloudEmbedUrl = (song) => {
    if (!song.link || !song.link.includes("soundcloud.com")) {
      return null;
    }

    const embedUrl = song.link.replace(
      "https://soundcloud.com/",
      "https://w.soundcloud.com/player/?url=https://soundcloud.com/"
    );
    return embedUrl;
  };

  const formatPlays = (plays) => {
    if (plays >= 1000000) {
      return (plays / 1000000).toFixed(1) + "M";
    } else if (plays >= 1000) {
      return (plays / 1000).toFixed(1) + "K";
    } else {
      return plays;
    }
  };

  return (
    <SongTableContainer>
      <ChartTitle>Top Chart</ChartTitle>
      <FilterContainer>
        {/* <div>
          <FilterLabel>Filter By:</FilterLabel>
          <FilterSelect value={filter} onChange={handleFilterChange}>
            <MenuItem value={"position"}>Position</MenuItem>
            <MenuItem value={"mostPlayed"}>Most Played</MenuItem>
            <MenuItem value={"newlyAdded"}>Newly Added</MenuItem>
          </FilterSelect>
        </div> */}
        <div>
          <FilterLabel>select tags:</FilterLabel>
          <FilterSelect value={selectedGenre} onChange={handleGenreChange}>
            <MenuItem value="tekkno">tekkno</MenuItem>
            <MenuItem value="hardstyle">hardstyle</MenuItem>
          </FilterSelect>
        </div>
        <div>
          <FilterLabel>Filter By Date:</FilterLabel>
          <FilterSelect value={selectedDate} onChange={handleDateChange}>
            <MenuItem value="all">All Dates</MenuItem>
            <MenuItem value="2023-01-01">2023-01-01</MenuItem>
            <MenuItem value="2023-02-01">2023-02-01</MenuItem>
            <MenuItem value="2023-03-01">2023-03-01</MenuItem>
            {/* Add more date options if needed */}
          </FilterSelect>
        </div>
      </FilterContainer>
      <TableContainerStyled component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <StyledTableHeadCell>Position</StyledTableHeadCell>
              <StyledTableHeadCell># 7d/ago</StyledTableHeadCell>
              <StyledTableHeadCell>Track-Name</StyledTableHeadCell>
              <StyledTableHeadCell>Genre</StyledTableHeadCell>
              <StyledTableCell>SoundCloud</StyledTableCell>

              <StyledTableHeadCell>Metrics</StyledTableHeadCell>
              <StyledTableHeadCell>Spotify-Search</StyledTableHeadCell>
              <StyledTableHeadCell>Spotify-Url</StyledTableHeadCell>

              <StyledTableHeadCell>Release-Date</StyledTableHeadCell>

              <StyledTableCell>Competitor-Track</StyledTableCell>
              <StyledTableCell>Competitor</StyledTableCell>
              <StyledTableCell>Competitor-Link</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredSongs.map((song) => (
              <TableRow key={song.current_position}>
                <PositionCell>
                  <span 
                  style={{
                    'marginLeft': 10,
                    'marginTop': 10
                  }}
                  >
                  {song.current_position}
                  </span>
                  <br  />
                  {song.previous_position === null ? (
                    <NewEntryIcon />
                  ) : song.previous_position < song.current_position ? (
                    <DownArrowIcon />
                  ) : song.previous_position > song.current_position ? (
                    <UpArrowIcon />
                  ) : null}
                </PositionCell>
                <SongTitleCell></SongTitleCell>
                <SongTitleCell>{song.title}</SongTitleCell>
                <StyledTableCell>{song.tags}</StyledTableCell>
                <StyledTableCell>
                  {song.link && song.link.includes("soundcloud.com") ? (
                    <iframe
                      title={song.title}
                      width="100%"
                      height="95"
                      scrolling="no"
                      frameBorder="no"
                      allow="autoplay"
                      src={getSoundCloudEmbedUrl(song)}
                    />
                  ) : null}
                </StyledTableCell>

                <StyledTableCell>
                  <span
                    style={{
                      display: "flex",
                      justifyContent: "space-around",
                      alignItems: "center",
                    }}
                  >
                    <LikeIcon /> {formatPlays(song.sound_likes)}
                  </span>

                  <br />
                  <span
                    style={{
                      display: "flex",
                      justifyContent: "space-around",
                      alignItems: "center",
                    }}
                  >
                    {" "}
                    <RepostIcon />
                    <p> {formatPlays(song.sound_repost)} </p>
                  </span>
                  <br />
                  <span
                    style={{
                      display: "flex",
                      justifyContent: "space-around",
                      alignItems: "center",
                    }}
                  >
                    {" "}
                    <PlayIcon /> {formatPlays(song.sound_play)}
                  </span>
                </StyledTableCell>
                <StyledTableCell>
                  <p>{song.spot_name}</p>
                </StyledTableCell>
                <StyledTableCell>
                  <p>{song.spot_url}</p>
                </StyledTableCell>
                <StyledTableCell>
                  {new Date(song.sound_release).toLocaleDateString()}
                </StyledTableCell>
                <StyledTableCell>{song.comp_name}</StyledTableCell>

                <StyledTableCell>{song.comp_artist}</StyledTableCell>
                <StyledTableCell>{song.comp_url}</StyledTableCell>
                <StyledTableCell>{song.song_time}</StyledTableCell>

                {/* <StyledTableCell>{song.likes}</StyledTableCell>
                <StyledTableCell>{song.reposts}</StyledTableCell> */}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainerStyled>
      <IframeContainer id="player-container"></IframeContainer>
    </SongTableContainer>
  );
};

export default SongTable;
