import {
    Text,
    HStack,
    Box,
    Avatar,
    Stack,
} from "@chakra-ui/react";

export default function ChatBox({ data }) {
    return data.map((item) => <MessageItem item={item} key={item}/>);
}

function MessageItem({ item }) {

    return (
        <Box mt="5">
            <HStack>
                <Avatar
                    bg="teal.400"
                    size="md"
                />{" "}
                <Stack>
                    <HStack spacing="20px">
                        <Text>
                            <b>You</b>
                        </Text>
                    </HStack>
                    <Text>{ item }</Text>
                </Stack>
            </HStack>
        </Box>
    );
}
