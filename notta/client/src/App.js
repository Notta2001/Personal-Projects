import { Container, Box } from '@mui/material';
import Header from './components/Header'
import { ThemeProvider } from '@mui/styles'
import { createTheme } from '@mui/system'

function App() {
  const theme = createTheme({
    palette: {
      background: {
        paper: "#1F2836",
        primary: "#1F2836",
        secondary: "#0F181A",
      },
      primary: { main: "#0FC8FF", light: "#A5EAFF" },
      text: {
        primary: "#0FC8FF",
        secondary: "#A5EAFF",
      },
    },
    breakpoints: {
      values: {
        xs: 0,
        sm: 576,
        md: 768,
        lg: 992,
        xl: 1200,
        xxl: 1400,
      },
    },
    overrides: {
      MuiCssBaseline: {
        "@global": {
          "*": {
            boxSizing: "border-box",
            margin: 0,
            padding: 0,
          },
          html: {
            "-webkit-font-smoothing": "antialiased",
            "-moz-osx-font-smoothing": "grayscale",
          },
          body: {
            fontFamily: "'Fira Sans', sans-serif",
            backgroundColor: "#1F2836",
          },
          ".second-font": {
            fontFamily: "'Fira Code', monospace",
          },
          "#root": {
            height: "100%",
            width: "100%",
          },
          ".MuiButtonBase-root.Mui-disabled": {
            cursor: "not-allowed",
            pointerEvents: "all",
          },
        },
      },
      MuiButton: {
        root: {
          textTransform: "none",
        },
      },
    },
  });

  return (
    <Box>
      <Header />
      <Container>
        Hello
      </ Container>
    </Box>
    
  );
}

export default App;
