import React, { useState } from "react";
import {
  Container,
  Box,
  VStack,
  Heading,
  Text,
  FormControl,
  FormLabel,
  Select,
  Button,
  useToast,
  useColorModeValue,
  ScaleFade,
  Divider,
  Badge,
  Flex,
  Spinner,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Card,
  CardBody,
  CardHeader,
  Icon,
} from "@chakra-ui/react";
import { useAuth } from "../contexts/AuthContext";
import { FaQuestionCircle, FaList, FaLightbulb } from "react-icons/fa";

function ContentGenerator() {
  const [subject, setSubject] = useState("");
  const [grade, setGrade] = useState("");
  const [loading, setLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [error, setError] = useState(null);
  const { currentUser } = useAuth();
  const toast = useToast();
  const bgColor = useColorModeValue("brand.50", "brand.900");
  const borderColor = useColorModeValue("brand.200", "brand.700");
  const textColor = useColorModeValue("brand.700", "brand.100");
  const cardBgColor = useColorModeValue("white", "brand.800");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!subject || !grade) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    setLoading(true);
    setGeneratedContent(null);
    setError(null);

    try {
      const response = await fetch(
        "http://localhost:5000/api/content/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            subject,
            grade,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to generate content");
      }

      setGeneratedContent(data.content);
      toast({
        title: "Success",
        description: "Content generated successfully",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      setError(error.message);
      toast({
        title: "Error",
        description: error.message,
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxW="container.md" py={10}>
      <VStack spacing={8}>
        <Box textAlign="center">
          <Heading color={textColor} size="2xl" mb={4}>
            Generate QCM Question
          </Heading>
          <Text fontSize="lg" color="brand.500">
            Create a single multiple choice question for your students
          </Text>
        </Box>

        {error && (
          <Alert status="error" borderRadius="md">
            <AlertIcon />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <Card
          w="100%"
          bg={bgColor}
          borderColor={borderColor}
          borderWidth={1}
          borderRadius="xl"
          boxShadow="lg"
        >
          <CardBody>
            <form onSubmit={handleSubmit}>
              <VStack spacing={6}>
                <FormControl isRequired>
                  <FormLabel color={textColor} fontSize="lg">
                    Subject
                  </FormLabel>
                  <Select
                    placeholder="Select subject"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    bg="white"
                    borderColor="brand.300"
                    size="lg"
                    _hover={{ borderColor: "brand.400" }}
                    _focus={{
                      borderColor: "brand.500",
                      boxShadow: "0 0 0 1px var(--chakra-colors-brand-500)",
                    }}
                  >
                    <option value="mathematics">Mathematics</option>
                    <option value="science">Science</option>
                    <option value="history">History</option>
                    <option value="literature">Literature</option>
                  </Select>
                </FormControl>

                <FormControl isRequired>
                  <FormLabel color={textColor} fontSize="lg">
                    Grade Level
                  </FormLabel>
                  <Select
                    placeholder="Select grade"
                    value={grade}
                    onChange={(e) => setGrade(e.target.value)}
                    bg="white"
                    borderColor="brand.300"
                    size="lg"
                    _hover={{ borderColor: "brand.400" }}
                    _focus={{
                      borderColor: "brand.500",
                      boxShadow: "0 0 0 1px var(--chakra-colors-brand-500)",
                    }}
                  >
                    <option value="elementary">Elementary</option>
                    <option value="middle">Middle School</option>
                    <option value="high">High School</option>
                  </Select>
                </FormControl>

                <Button
                  type="submit"
                  colorScheme="brand"
                  width="100%"
                  size="lg"
                  isLoading={loading}
                  bg="brand.400"
                  _hover={{ bg: "brand.500" }}
                  loadingText="Generating..."
                  spinner={<Spinner color="white" />}
                >
                  Generate Question
                </Button>
              </VStack>
            </form>
          </CardBody>
        </Card>

        <ScaleFade in={!!generatedContent} initialScale={0.9}>
          {generatedContent && (
            <Card
              w="100%"
              bg={cardBgColor}
              borderColor={borderColor}
              borderWidth={1}
              borderRadius="xl"
              boxShadow="xl"
            >
              <CardHeader>
                <Heading size="md" color={textColor}>
                  Generated Question
                </Heading>
              </CardHeader>

              <CardBody>
                <VStack spacing={6} align="stretch">
                  {/* Question */}
                  <Box p={4} bg="brand.50" borderRadius="md">
                    <Text fontSize="lg" fontWeight="bold" mb={2}>
                      Question:
                    </Text>
                    <Text fontSize="md">{generatedContent.question}</Text>
                  </Box>

                  {/* Options */}
                  <Box p={4} bg="brand.50" borderRadius="md">
                    <Text fontSize="lg" fontWeight="bold" mb={2}>
                      Options:
                    </Text>
                    <VStack spacing={2} align="stretch">
                      {generatedContent.options.map((option, index) => (
                        <Box
                          key={index}
                          p={2}
                          bg="white"
                          borderRadius="md"
                          borderWidth={1}
                          borderColor="brand.200"
                        >
                          <Text>
                            {index + 1}. {option}
                          </Text>
                        </Box>
                      ))}
                    </VStack>
                  </Box>

                  {/* Explanation */}
                  <Box p={4} bg="brand.50" borderRadius="md">
                    <Text fontSize="lg" fontWeight="bold" mb={2}>
                      Explanation:
                    </Text>
                    <Text fontSize="md">{generatedContent.explanation}</Text>
                  </Box>
                </VStack>
              </CardBody>
            </Card>
          )}
        </ScaleFade>
      </VStack>
    </Container>
  );
}

export default ContentGenerator;
