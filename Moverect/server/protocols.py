class Protocols:
    class Response:
        NICKNAME = "protocol.request_nickname"
        QUESTIONS = "protocol.questions"
        START = "protocol.start"
        PLAYERS_POS = "protocol.player_pos"
        PLAYER_LEFT = "protocol.player_left"

    class Request:
        PLAYER_MOVEMENT = "protocol.player_movement"
        NICKNAME = "protocol.send_nickname"
        LEAVE = "protocol.leave"