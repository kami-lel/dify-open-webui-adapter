# Hack rm


class _SSEType(Flag):
    """
    represent a single **relevant** SSE specified by Dify Backend API
    """

    # pylint: disable=invalid-name

    # events we don't care about
    IRRELEVANT = 0

    # enum name specified by Dify Backend API
    text_chunk = auto()
    message = auto()
    workflow_finished = auto()
    message_end = auto()

    # events which indicate end of  current round response
    IS_END = workflow_finished | message_end

    def __bool__(self):
        """
        :return: whether event is a relevant event
        :rtype: bool
        """
        return self != self.IRRELEVANT


class _StreamingConversationRound:
    """
    represent a single conversation round with Dify


    :raises ValueError:
    :raises UnicodeDecodeError:
    :raises json.JSONDecodeError:
    :raises KeyError:
    """

    _TEXT_STREAM_ENCODING = "utf-8"
    _STREAM_PREFIX = "data: "

    def __init__(self, app):
        self.app = app
        # cache the response for closing when finished this round
        self.response = self.app.open_reply_response()
        self.iter_lines = self.response.iter_lines()

    # implement iter()  ========================================================

    def __iter__(self):
        return self  # make self an Iterator

    def __next__(self):
        debug_lines = ["\n"]

        text = None
        event = _SSEType.IRRELEVANT  # default

        # consume self.iter_lines until find relevant events
        while not event:
            try:
                raw = next(self.iter_lines)

                line = raw.decode(self._TEXT_STREAM_ENCODING)
                if DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE:
                    debug_lines.append(line)

                # deal with data: prefix
                if not line.startswith(self._STREAM_PREFIX):
                    continue  # not start w/ "data: ", skip
                line = line[len(self._STREAM_PREFIX) :]

                # parse data as JSON
                data = json.loads(line)
                event_value = data["event"]

                # deal with only relevant types of SSE
                try:
                    event = _SSEType[event_value]
                except KeyError:  # not a relevant event
                    continue

                # extract text
                if event is _SSEType.message:
                    text = data["answer"]
                elif event is _SSEType.text_chunk:
                    text = data["data"]["text"]

                # extract conversation_id for Chatflow, if it's empty
                if (
                    isinstance(self.app, ChatflowApp)
                    and not self.app.conversation_id
                ):
                    self.app.conversation_id = data["conversation_id"]

            except StopIteration as err:
                raise ValueError(
                    "exhaust text/event-stream without ending event"
                ) from err

            except UnicodeDecodeError as err:
                err.args = (
                    "fail to decode text/event-stream: {}".format(str(err)),
                    *(err.args[1:]),
                )
                raise  # re-raise

            except JSONDecodeError as err:
                err.args = (
                    "fail to parse text/event-stream as JSON: {}: {}".format(
                        err.args[0], raw
                    ),
                    *(err.args[1:]),
                )
                raise  # re-raise

            except KeyError as err:
                raise KeyError(
                    "miss key in text/event-stream content: {}".format(str(err))
                ) from err

        # an relevant event is found  ------------------------------------------

        if event in _SSEType.IS_END:  # end of current respond
            if DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE:
                debug_lines.insert(1, "# LAST PASS")
                return "\n\n".join(debug_lines)

            self.response.close()
            raise StopIteration

        if DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE:
            debug_lines.insert(1, "# PASS")
            return "\n\n".join(debug_lines)

        # a text chunk as part of current respond
        return text
