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
import { ChatIcon, DownloadIcon, CheckCircleIcon } from '@chakra-ui/icons';
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
    
    console.log("obama: ")
    console.log("note: ", note)

    setSavedNotes(savedNotes => [...savedNotes, note]); // Using the functional form of setState
    
    console.log([...savedNotes, note])

    // fetch for sending data
    // Making an AJAX request to Flask backend
    fetch('/send-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify([...savedNotes, note])
    })
    .then(response => {
      // Handle response if needed
      console.log('Data sent successfully');
    })
    .catch(error => {
      // Handle error if needed
      console.error('Error sending data:', error);
    });
    setNote('');
  };

  // fetch members from backend to frontend, should re-render
  useEffect(() => {
    fetch('/members')
      .then(res => res.json())
      .then(data => {
        // call setData
        setData(data);
        console.log("shrek");
        console.log(data);
      });
  }, [savedNotes]);

  return (
    <ChakraProvider>
      <Center
        color="black"
        backgroundColor="teal"
        bgGradient="linear(to-l, teal.600, blue.600)"
      >
        <Image
          mt="20px"
          borderRadius='full'
          boxSize='100px'
          src='https://i.imgur.com/iLMAeW1.png'
        />

        
        <Heading
          ml="20px"
          mt="20px"
          mb="10px"
          color="white"
          fontSize="6xl"
          fontWeight="extrabold"
          size="6xl"
        >
          Tuberculosis AI Pre-Screening
        </Heading>
      </Center>

      <Center color="white" bgGradient="linear(to-l, teal.600, blue.600)">
        <Text mb="30px" fontSize="xl">
          Generative AI and speech-to-text to detect potential TB cases and
          create a report for doctors
        </Text>
      </Center>

      <Center mt="100px" mb="100px" color="black">
        <HStack spacing="20px">
          <Avatar
            size="lg"
            src="https://i.imgur.com/IO3XefC.png"
          />
          <TypeIt options={{ speed: 30, waitUntilVisible: true, }} style={{ fontSize: "36px" }}>
            <b>Hello!</b> Tell me about yourself and your symptoms by reporting them below.
          </TypeIt>
        </HStack>
      </Center>

      <Center>
        <Card align="center" width="700px" mb="10px">
          <CardHeader>
            {isListening ? (
              <Heading size="lg">
                Voice Input 🔴
              </Heading>
            ) : (
              <Heading size="lg">
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
                <HStack>
                  <Button
                    rightIcon={<ChatIcon />}
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

                  {isListening || note == null ? (
                    <Text>Wait a couple seconds before speaking</Text>
                  ) : (
                    <HStack>
                      <Button
                      rightIcon={<CheckCircleIcon />}
                      colorScheme="green"
                      size="lg"
                      onClick={handleSaveNote}
                    >
                      Submit Answer
                    </Button>

                    <Button
                      rightIcon={<DownloadIcon />}
                      colorScheme="blue"
                      size="lg"
                      onClick={handleSaveNote} // to do later
                    >
                      Generate PDF
                    </Button>
                    </HStack>
                  )}
                </HStack>
              </Center>
            </VStack>
          </CardFooter>
        </Card>
      </Center>

      <Center mt="50px">
        <Stack>
          <HStack width="50%" maxWidth="6xl">
            <Stack>
              <Text fontSize="3xl">
                  <b>Your Responses</b>
              </Text>
              <Divider></Divider>
              <Box
                  overflowY="auto"
                  maxHeight="150px"
                  minWidth="6xl"
              >
                  <ChatBox data={savedNotes} />
              </Box>
            </Stack>
          </HStack>
        </Stack>
      </Center>

      {/* <div>
        {typeof data === 'undefined' ? (
          <p>Loading...</p>
        ) : (
          data.map((member, i) => <p key={i}>{JSON.stringify(member)}</p>)
        )}
      </div> */}
      {/* <div className="box">
        <h2>Notes</h2>
        {savedNotes.map(n => (
          <p key={n}>{n}</p>
        ))}
      </div> */}
    </ChakraProvider>
  );
}

export default App;
