import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ChakraProvider, CSSReset, extendTheme } from "@chakra-ui/react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ContentGenerator from "./pages/ContentGenerator";
import PrivateRoute from "./components/PrivateRoute";

// Thème personnalisé avec des couleurs féminines
const theme = extendTheme({
  colors: {
    brand: {
      50: "#FFF0F5", // Rose très clair
      100: "#FFE4E9", // Rose clair
      200: "#FFC0CB", // Rose pâle
      300: "#FFB6C1", // Rose clair
      400: "#FF69B4", // Rose vif
      500: "#FF1493", // Rose profond
      600: "#DB7093", // Rose moyen
      700: "#C71585", // Rose foncé
      800: "#8B008B", // Rose très foncé
      900: "#4B0082", // Indigo foncé
    },
  },
  components: {
    Button: {
      defaultProps: {
        colorScheme: "brand",
      },
    },
    Link: {
      baseStyle: {
        color: "brand.500",
        _hover: {
          color: "brand.600",
          textDecoration: "none",
        },
      },
    },
  },
  styles: {
    global: {
      body: {
        bg: "brand.50",
        color: "gray.800",
      },
    },
  },
});

function App() {
  return (
    <ChakraProvider theme={theme}>
      <CSSReset />
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/generate"
            element={
              <PrivateRoute>
                <ContentGenerator />
              </PrivateRoute>
            }
          />
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;
