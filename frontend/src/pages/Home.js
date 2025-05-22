import React from "react";
import {
  Box,
  Container,
  Heading,
  Text,
  Button,
  VStack,
  useColorModeValue,
} from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";

function Home() {
  const bgColor = useColorModeValue("brand.50", "brand.900");
  const textColor = useColorModeValue("brand.700", "brand.100");

  return (
    <Container maxW="container.xl" py={20}>
      <VStack spacing={8} textAlign="center">
        <Heading as="h1" size="2xl" color={textColor}>
          Welcome to Content Generator
        </Heading>
        <Text fontSize="xl" color={textColor}>
          Generate high-quality content for your needs with our AI-powered
          platform
        </Text>
        <Button
          as={RouterLink}
          to="/register"
          colorScheme="brand"
          size="lg"
          bg="brand.400"
          _hover={{ bg: "brand.500" }}
        >
          Get Started
        </Button>
      </VStack>
    </Container>
  );
}

export default Home;
