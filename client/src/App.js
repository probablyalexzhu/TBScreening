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
import { ChatIcon, CloseIcon } from '@chakra-ui/icons';
import { useState, useEffect } from 'react';

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition
const mic = new SpeechRecognition()

mic.continuous = true
mic.interimResults = true
mic.lang = 'fr'

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
  const [isListening, setIsListening] = useState(false)
  const [note, setNote] = useState(null)
  const [savedNotes, setSavedNotes] = useState([])

  useEffect(() => {
    handleListen()
  }, [isListening])

  const handleListen = () => {
    if (isListening) {
      mic.start()
      mic.onend = () => {
        console.log('continue..')
        mic.start()
      }
    } else {
      mic.stop()
      mic.onend = () => {
        console.log('Stopped Mic on Click')
      }
    }
    mic.onstart = () => {
      console.log('Mics on')
    }

    mic.onresult = event => {
      const transcript = Array.from(event.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('')
      console.log(transcript)
      setNote(transcript)
      mic.onerror = event => {
        console.log(event.error)
      }
    }
  }

  const handleSaveNote = () => {
    setSavedNotes([...savedNotes, note])
    setNote('')
  }

  return (
    <ChakraProvider>
      <Center mt="50px" color="black">
        <Heading
          bgGradient="linear(to-l, teal.500, green.500)"
          bgClip="text"
          fontSize="6xl"
          fontWeight="extrabold"
          size="6xl"
        >
          India Tuberculosis AI Pre-Screener
        </Heading>
      </Center>

      <Center mt="50px" mb="50px" color="black">
        <Text fontSize="2xl">
          Pre-screening with generative AI and text-to-speech to alert potential
          TB cases and create a report for doctors
        </Text>
      </Center>

      <Center mt="100px" mb="100px" color="black">
        <Text>
          Hello! Tell me about yourself and your symptoms by reporting them below.
        </Text>
      </Center>

      <Center>
        <Stack>
          <Avatar />
          <Card>
            <CardBody>
              <Text>
                {note}
              </Text>
            </CardBody>
          </Card>
        </Stack>
        </Center>

        <VStack>
        <Center>
          <VStack mt="50px">
            {isListening ? <span>🎙️</span> : <span>🛑🎙️</span>}
            <Button
              leftIcon={<ChatIcon />}
              color="green"
              size="lg"
              onClick={() => setIsListening(prevState => !prevState)}
            >
              Start/Stop Recording Answer
            </Button>
            <Button
              leftIcon={<CloseIcon />}
              color="red"
              size="lg"
              onClick={handleSaveNote}
            >
              Save Answer
            </Button>
          </VStack>
        </Center>
      </VStack>
      <div>
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
        </div>
    </ChakraProvider>
  );
}

export default App;