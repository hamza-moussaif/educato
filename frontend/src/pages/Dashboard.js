import React from "react";
import { useNavigate } from "react-router-dom";
import {
  Container,
  Heading,
  Text,
  Button,
  VStack,
  Box,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  useColorModeValue,
} from "@chakra-ui/react";
import { useAuth } from "../contexts/AuthContext";

function Dashboard() {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const bgColor = useColorModeValue("brand.50", "brand.900");
  const borderColor = useColorModeValue("brand.200", "brand.700");
  const textColor = useColorModeValue("brand.700", "brand.100");
  const statBgColor = useColorModeValue("white", "brand.800");

  return (
    <Container maxW="container.xl" py={10}>
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading size="lg" color={textColor}>
            Welcome, {currentUser?.name}!
          </Heading>
          <Text mt={2} color="brand.500">
            Manage your content generation and view your history
          </Text>
        </Box>

        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
          <Stat
            px={4}
            py={5}
            shadow="base"
            borderColor={borderColor}
            rounded="lg"
            bg={statBgColor}
          >
            <StatLabel color={textColor}>Total Generations</StatLabel>
            <StatNumber color="brand.500">0</StatNumber>
            <StatHelpText color={textColor}>Since you joined</StatHelpText>
          </Stat>

          <Stat
            px={4}
            py={5}
            shadow="base"
            borderColor={borderColor}
            rounded="lg"
            bg={statBgColor}
          >
            <StatLabel color={textColor}>Credits Remaining</StatLabel>
            <StatNumber color="brand.500">100</StatNumber>
            <StatHelpText color={textColor}>Free credits</StatHelpText>
          </Stat>

          <Stat
            px={4}
            py={5}
            shadow="base"
            borderColor={borderColor}
            rounded="lg"
            bg={statBgColor}
          >
            <StatLabel color={textColor}>Last Generation</StatLabel>
            <StatNumber color="brand.500">-</StatNumber>
            <StatHelpText color={textColor}>No generations yet</StatHelpText>
          </Stat>
        </SimpleGrid>

        <Box textAlign="center" mt={8}>
          <Button
            colorScheme="brand"
            size="lg"
            onClick={() => navigate("/generate")}
            bg="brand.400"
            _hover={{ bg: "brand.500" }}
          >
            Generate New Content
          </Button>
        </Box>
      </VStack>
    </Container>
  );
}

export default Dashboard;
