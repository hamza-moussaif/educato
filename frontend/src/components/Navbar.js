import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { Box, Flex, Link, Button, useColorModeValue } from "@chakra-ui/react";
import { useAuth } from "../contexts/AuthContext";

function Navbar() {
  const { currentUser, logout } = useAuth();
  const bgColor = useColorModeValue("brand.100", "brand.800");
  const borderColor = useColorModeValue("brand.200", "brand.700");

  return (
    <Box
      bg={bgColor}
      px={4}
      borderBottom="1px"
      borderColor={borderColor}
      boxShadow="sm"
    >
      <Flex h={16} alignItems="center" justifyContent="space-between">
        <Flex alignItems="center">
          <Link
            as={RouterLink}
            to="/"
            fontWeight="bold"
            fontSize="xl"
            color="brand.600"
          >
            Content Generator
          </Link>
        </Flex>

        <Flex alignItems="center" gap={4}>
          {currentUser ? (
            <>
              <Link
                as={RouterLink}
                to="/dashboard"
                color="brand.600"
                _hover={{ color: "brand.500" }}
              >
                Dashboard
              </Link>
              <Link
                as={RouterLink}
                to="/generate"
                color="brand.600"
                _hover={{ color: "brand.500" }}
              >
                Generate Content
              </Link>
              <Button onClick={logout} variant="outline" colorScheme="brand">
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link
                as={RouterLink}
                to="/login"
                color="brand.600"
                _hover={{ color: "brand.500" }}
              >
                Login
              </Link>
              <Link
                as={RouterLink}
                to="/register"
                color="brand.600"
                _hover={{ color: "brand.500" }}
              >
                Register
              </Link>
            </>
          )}
        </Flex>
      </Flex>
    </Box>
  );
}

export default Navbar;
