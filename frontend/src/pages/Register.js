import React, { useState } from "react";
import { useNavigate, Link as RouterLink } from "react-router-dom";
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  Text,
  Link,
  useToast,
  Container,
  useColorModeValue,
} from "@chakra-ui/react";
import { useAuth } from "../contexts/AuthContext";

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();
  const bgColor = useColorModeValue("brand.50", "brand.900");
  const borderColor = useColorModeValue("brand.200", "brand.700");
  const textColor = useColorModeValue("brand.700", "brand.100");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await register(username, email, password);
      navigate("/dashboard");
    } catch (error) {
      const errorMessage = error.response?.data?.error || "Failed to register";
      toast({
        title: "Error",
        description: errorMessage,
        status: "error",
        duration: 5000,
        isClosable: true,
      });

      // Si l'email est déjà enregistré, vider le champ email
      if (errorMessage === "Email already registered") {
        setEmail("");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxW="container.sm" py={20}>
      <VStack spacing={8}>
        <Heading color={textColor}>Register</Heading>
        <Box
          w="100%"
          p={8}
          borderWidth={1}
          borderRadius="lg"
          bg={bgColor}
          borderColor={borderColor}
        >
          <form onSubmit={handleSubmit}>
            <VStack spacing={4}>
              <FormControl isRequired>
                <FormLabel color={textColor}>Username</FormLabel>
                <Input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  borderColor="brand.300"
                  _hover={{ borderColor: "brand.400" }}
                  _focus={{
                    borderColor: "brand.500",
                    boxShadow: "0 0 0 1px var(--chakra-colors-brand-500)",
                  }}
                />
              </FormControl>
              <FormControl isRequired>
                <FormLabel color={textColor}>Email</FormLabel>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  borderColor="brand.300"
                  _hover={{ borderColor: "brand.400" }}
                  _focus={{
                    borderColor: "brand.500",
                    boxShadow: "0 0 0 1px var(--chakra-colors-brand-500)",
                  }}
                />
              </FormControl>
              <FormControl isRequired>
                <FormLabel color={textColor}>Password</FormLabel>
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  borderColor="brand.300"
                  _hover={{ borderColor: "brand.400" }}
                  _focus={{
                    borderColor: "brand.500",
                    boxShadow: "0 0 0 1px var(--chakra-colors-brand-500)",
                  }}
                />
              </FormControl>
              <Button
                type="submit"
                colorScheme="brand"
                width="100%"
                isLoading={loading}
                bg="brand.400"
                _hover={{ bg: "brand.500" }}
              >
                Register
              </Button>
            </VStack>
          </form>
        </Box>
        <Text color={textColor}>
          Already have an account?{" "}
          <Link
            as={RouterLink}
            to="/login"
            color="brand.500"
            _hover={{ color: "brand.600" }}
          >
            Login here
          </Link>
        </Text>
      </VStack>
    </Container>
  );
}

export default Register;
