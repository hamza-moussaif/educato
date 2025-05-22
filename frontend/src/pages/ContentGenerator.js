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
  Radio,
  RadioGroup,
  Stack,
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
  Link,
} from "@chakra-ui/react";
import { useAuth } from "../contexts/AuthContext";

function ContentGenerator() {
  const [subject, setSubject] = useState("");
  const [grade, setGrade] = useState("");
  const [contentType, setContentType] = useState("quiz");
  const [loading, setLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
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
    setSelectedAnswer(null);
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
            content_type: contentType,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        if (
          data.error &&
          data.error.includes("Timeout while connecting to Ollama API")
        ) {
          throw new Error(
            "The AI service is currently unavailable. Please make sure Ollama is running and try again."
          );
        }
        throw new Error(
          data.error || data.message || "Failed to generate content"
        );
      }

      if (data.message === "This endpoint accepts POST requests") {
        throw new Error("API endpoint is not properly configured");
      }

      setGeneratedContent(data.content || data);
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

  const checkAnswer = () => {
    if (selectedAnswer === null) {
      toast({
        title: "Warning",
        description: "Please select an answer",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    const isCorrect = selectedAnswer === generatedContent.correct_answer;
    toast({
      title: isCorrect ? "Correct!" : "Incorrect",
      description: generatedContent.explanation,
      status: isCorrect ? "success" : "error",
      duration: 5000,
      isClosable: true,
    });
  };

  return (
    <Container maxW="container.md" py={10}>
      <VStack spacing={8}>
        <Box textAlign="center">
          <Heading color={textColor}>Generate Educational Content</Heading>
          <Text mt={2} color="brand.500">
            Create personalized educational content for your students
          </Text>
        </Box>

        {error && (
          <Alert
            status="error"
            borderRadius="md"
            flexDirection="column"
            alignItems="flex-start"
            p={4}
          >
            <Flex>
              <AlertIcon />
              <AlertTitle>Error</AlertTitle>
            </Flex>
            <AlertDescription mt={2}>
              {error}
              {error.includes("Ollama") && (
                <Box mt={2}>
                  <Text fontSize="sm">To fix this issue:</Text>
                  <Text fontSize="sm" mt={1}>
                    1. Make sure Ollama is installed and running
                  </Text>
                  <Text fontSize="sm">
                    2. Run <code>ollama pull mistral</code> in your terminal
                  </Text>
                  <Text fontSize="sm">3. Restart the Flask server</Text>
                  <Text fontSize="sm" mt={2}>
                    Need help? Check the{" "}
                    <Link
                      href="https://github.com/ollama/ollama"
                      color="brand.500"
                      isExternal
                    >
                      Ollama documentation
                    </Link>
                  </Text>
                </Box>
              )}
            </AlertDescription>
          </Alert>
        )}

        <Box
          w="100%"
          p={8}
          borderWidth={1}
          borderRadius="lg"
          bg={bgColor}
          borderColor={borderColor}
          boxShadow="sm"
          transition="all 0.3s"
          _hover={{ boxShadow: "md" }}
        >
          <form onSubmit={handleSubmit}>
            <VStack spacing={6}>
              <FormControl isRequired>
                <FormLabel color={textColor}>Subject</FormLabel>
                <Select
                  placeholder="Select subject"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  bg="white"
                  borderColor="brand.300"
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
                <FormLabel color={textColor}>Grade Level</FormLabel>
                <Select
                  placeholder="Select grade"
                  value={grade}
                  onChange={(e) => setGrade(e.target.value)}
                  bg="white"
                  borderColor="brand.300"
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

              <FormControl>
                <FormLabel color={textColor}>Content Type</FormLabel>
                <RadioGroup value={contentType} onChange={setContentType}>
                  <Stack direction="row" spacing={4}>
                    <Radio value="quiz" colorScheme="brand">
                      Quiz
                    </Radio>
                    <Radio value="lesson" colorScheme="brand">
                      Lesson Plan
                    </Radio>
                    <Radio value="exercise" colorScheme="brand">
                      Exercise
                    </Radio>
                  </Stack>
                </RadioGroup>
              </FormControl>

              <Button
                type="submit"
                colorScheme="brand"
                width="100%"
                isLoading={loading}
                bg="brand.400"
                _hover={{ bg: "brand.500" }}
                loadingText="Generating..."
                spinner={<Spinner color="white" />}
              >
                Generate Content
              </Button>
            </VStack>
          </form>
        </Box>

        <ScaleFade in={!!generatedContent} initialScale={0.9}>
          {generatedContent && (
            <Box
              w="100%"
              p={8}
              borderWidth={1}
              borderRadius="lg"
              bg={cardBgColor}
              borderColor={borderColor}
              boxShadow="md"
            >
              <VStack spacing={6} align="stretch">
                <Flex justify="space-between" align="center">
                  <Heading size="md" color={textColor}>
                    {contentType.charAt(0).toUpperCase() + contentType.slice(1)}
                  </Heading>
                  <Badge colorScheme="brand" fontSize="sm">
                    {grade.charAt(0).toUpperCase() + grade.slice(1)}
                  </Badge>
                </Flex>

                <Divider borderColor={borderColor} />

                <Box>
                  <Text fontSize="lg" color={textColor} mb={4}>
                    {generatedContent.question || generatedContent.content}
                  </Text>

                  {generatedContent.options && (
                    <RadioGroup
                      onChange={(value) => setSelectedAnswer(parseInt(value))}
                      value={selectedAnswer}
                    >
                      <Stack spacing={4}>
                        {generatedContent.options.map((option, index) => (
                          <Radio
                            key={index}
                            value={index.toString()}
                            colorScheme="brand"
                            borderColor="brand.300"
                            _hover={{ borderColor: "brand.400" }}
                          >
                            {option}
                          </Radio>
                        ))}
                      </Stack>
                    </RadioGroup>
                  )}

                  {generatedContent.options && (
                    <Button
                      mt={6}
                      colorScheme="brand"
                      onClick={checkAnswer}
                      isDisabled={selectedAnswer === null}
                      bg="brand.400"
                      _hover={{ bg: "brand.500" }}
                    >
                      Check Answer
                    </Button>
                  )}
                </Box>
              </VStack>
            </Box>
          )}
        </ScaleFade>
      </VStack>
    </Container>
  );
}

export default ContentGenerator;
