import React from 'react';
import {
  Avatar,
  CardHeader,
  CardFooter,
  Textarea,
  ChakraProvider,
  Box,
  Text,
  Link,
  VStack,
  Code,
  Grid,
  Button,
  ButtonGroup,
  theme,
  Center,
  Heading,
  HStack,
  Divider,
  Card,
  Stack,
  CardBody,
  Image,
} from '@chakra-ui/react';
import { ChatIcon, CloseIcon, CheckCircleIcon } from '@chakra-ui/icons';
import { useState, useEffect } from 'react';
import ChatBox from './components/ChatBox';
import TypeIt from "typeit-react";

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const mic = new SpeechRecognition();

mic.continuous = true;
mic.interimResults = true;
mic.lang = 'en-US';

function App() {
  // store data from backend in data
  const [data, setData] = useState([{}]);

  // fetch members from backend to frontend, should re-render
  useEffect(() => {
    fetch('/members')
      .then(res => res.json())
      .then(data => {
        // call setData
        setData(data);
        console.log(data);
      });
  }, []);

  // audio stuff
  const [isListening, setIsListening] = useState(false);
  const [note, setNote] = useState(null);
  const [savedNotes, setSavedNotes] = useState([]);

  useEffect(() => {
    handleListen();
  }, [isListening]);

  const handleListen = () => {
    if (isListening) {
      mic.start();
      mic.onend = () => {
        console.log('continue..');
        mic.start();
      };
    } else {
      mic.stop();
      mic.onend = () => {
        console.log('Stopped Mic on Click');
      };
    }
    mic.onstart = () => {
      console.log('Mics on');
    };

    mic.onresult = event => {
      const transcript = Array.from(event.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('');
      console.log(transcript);
      setNote(transcript);
      mic.onerror = event => {
        console.log(event.error);
      };
    };
  };

  const handleSaveNote = () => {
    setSavedNotes([...savedNotes, note]);
    setNote('');
  };

  return (
    <ChakraProvider>
      <Center
        color="black"
        backgroundColor="teal"
        bgGradient="linear(to-l, teal.600, blue.600)"
      >
        <Heading
          mt="40px"
          mb="10px"
          color="white"
          fontSize="6xl"
          fontWeight="extrabold"
          size="6xl"
        >
          Tuberculosis AI Pre-Screener
        </Heading>
      </Center>

      <Center color="white" bgGradient="linear(to-l, teal.600, blue.600)">
        <Text mb="40px" fontSize="xl">
          Generative AI and speech-to-text to detect potential TB cases and
          create a report for doctors
        </Text>
      </Center>

      <Center mt="100px" mb="100px" color="black">
        <TypeIt options={{ speed: 30, waitUntilVisible: true, }} style={{ fontSize: "36px" }}>
          <b>Hello!</b> Tell me about yourself and your symptoms by reporting them below.
        </TypeIt>
      </Center>

      <Center>
        <ChatBox data={savedNotes} />
      </Center>

      <Center>
        <Card align="center" width="600px">
          <CardHeader>
            {isListening ? (
              <Heading size="md">
                Voice Input 🔴
              </Heading>
            ) : (
              <Heading size="md">
              Voice Input 🎙️
              </Heading>
            )}
          </CardHeader>
          <CardBody>
            <Text color={"blue.600"}>{note}</Text>
          </CardBody>
          <CardFooter>
            <VStack>
              <Center>
                <VStack>
                  <Button
                    leftIcon={<ChatIcon />}
                    variant="solid"
                    colorScheme="red"
                    size="lg"
                    onClick={() => setIsListening(prevState => !prevState)}
                  >
                    {isListening ? (
                      <span>Stop Recording</span>
                    ) : (
                      <span>Start Recording</span>
                    )}
                  </Button>

                  {isListening ? (
                    <Button
                    isLoading
                    colorScheme="green"
                    size="lg"
                    > A Submit Answer
                    </Button>
                  ) : (
                    <Button
                      leftIcon={<CheckCircleIcon />}
                      colorScheme="green"
                      size="lg"
                      onClick={handleSaveNote}
                    >
                      Submit Answer
                    </Button>
                  )}
                </VStack>
              </Center>
            </VStack>
          </CardFooter>
        </Card>
      </Center>

      {/* <div>
        {typeof data.members === 'undefined' ? (
          <p>Loading...</p>
        ) : (
          data.members.map((member, i) => <p key={i}>{member}</p>)
        )}
      </div>
      <div className="box">
        <h2>Notes</h2>
        {savedNotes.map(n => (
          <p key={n}>{n}</p>
        ))}
      </div> */}
    </ChakraProvider>
  );
}

export default App;
