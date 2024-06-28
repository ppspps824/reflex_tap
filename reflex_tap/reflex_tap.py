import asyncio
import random

import reflex as rx

BUTTON_NUM = 5
GAME_DURATION = 20  # Game duration in seconds

BUTTON_WIDTH = "80px"


class ButtonState(rx.State):
    button_visibility: dict[str, bool] = {
        f"button{num}": True for num in range(BUTTON_NUM)
    }
    button_positions: dict[str, dict[str, str]] = {}
    special_button_visible: bool = False
    special_button_position: dict[str, str] = {"top": "0vh", "left": "0vw"}
    penalty_button_visible: bool = False
    penalty_button_position: dict[str, str] = {"top": "0vh", "left": "0vw"}
    score: int = 0
    time_remaining: int = GAME_DURATION
    game_active: bool = False

    def hide_button(self, button_id: str):
        if not self.game_active:
            return None
        self.button_visibility[button_id] = False
        self.score += 1
        if all(not visibility for visibility in self.button_visibility.values()):
            self.generate_positions()

        return rx.call_script("playFromStart('button_sfx')")

    def hide_special_button(self):
        if not self.game_active:
            return None
        self.special_button_visible = False
        self.score += 3

        return rx.call_script("playFromStart('button_sfx2')")

    def hide_penalty_button(self):
        if not self.game_active:
            return None
        self.penalty_button_visible = False
        self.score = max(0, self.score - 5)
        return rx.call_script("playFromStart('penalty_sfx')")

    def generate_positions(self):
        new_positions = {}
        for button_id in self.button_visibility.keys():
            new_positions[button_id] = {
                "top": f"{random.randint(10, 90)}vh",
                "left": f"{random.randint(10, 90)}vw",
            }
        self.button_positions = new_positions
        self.button_visibility = {key: True for key in self.button_visibility}

        if random.random() < 0.3:  # 30% chance to show special button
            self.special_button_visible = True
            self.special_button_position = {
                "top": f"{random.randint(10, 90)}vh",
                "left": f"{random.randint(10, 90)}vw",
            }
        else:
            self.special_button_visible = False

        if random.random() < 0.9:  # 20% chance to show penalty button
            self.penalty_button_visible = True
            self.penalty_button_position = {
                "top": f"{random.randint(10, 90)}vh",
                "left": f"{random.randint(10, 90)}vw",
            }
        else:
            self.penalty_button_visible = False

    def start_game(self):
        self.score = 0
        self.time_remaining = GAME_DURATION
        self.game_active = True
        self.generate_positions()
        return [ButtonState.tick, rx.call_script("playBGM()")]

    @rx.background
    async def tick(self):
        while self.game_active and self.time_remaining > 0:
            await asyncio.sleep(1)
            async with self:
                self.time_remaining -= 1
        if self.time_remaining == 0:
            async with self:
                self.game_active = False
                self.bgm_playing = False
            return rx.call_script("stopBGM()")


def button(info: tuple[str, bool]):
    return rx.cond(
        info[1],
        rx.button(
            rx.chakra.image(
                src="/button.png",
                loading="lazy",
                border_radius="full",
                width=BUTTON_WIDTH,
            ),
            on_click=ButtonState.hide_button(info[0]),
            position="absolute",
            top=rx.cond(
                ButtonState.button_positions.contains(info[0]),
                ButtonState.button_positions[info[0]]["top"],
                "0vh",
            ),
            left=rx.cond(
                ButtonState.button_positions.contains(info[0]),
                ButtonState.button_positions[info[0]]["left"],
                "0vw",
            ),
            variant="ghost",
        ),
        rx.text(""),
    )


def special_button():
    return rx.cond(
        ButtonState.special_button_visible,
        rx.button(
            rx.chakra.image(
                src="/special.webp",
                loading="lazy",
                border_radius="full",
                width=BUTTON_WIDTH,
            ),
            on_click=ButtonState.hide_special_button,
            position="absolute",
            top=ButtonState.special_button_position["top"],
            left=ButtonState.special_button_position["left"],
            variant="ghost",
        ),
        rx.text(""),
    )


def penalty_button():
    return rx.cond(
        ButtonState.penalty_button_visible,
        rx.button(
            rx.chakra.image(
                src="/penalty.webp",
                loading="lazy",
                border_radius="full",
                width=BUTTON_WIDTH,
            ),
            on_click=ButtonState.hide_penalty_button,
            position="absolute",
            top=ButtonState.penalty_button_position["top"],
            left=ButtonState.penalty_button_position["left"],
            variant="ghost",
        ),
        rx.text(""),
    )


@rx.page(route="/", title="Tap!Tap!Tap!")
def index():
    return rx.box(
        rx.cond(
            ~ButtonState.game_active & ButtonState.time_remaining,
            rx.box(
                rx.chakra.image(
                    src="/top.webp",
                    object_fit="cover",
                    loading="lazy",
                    width="100%",
                    height="100vh",  # 画面の高さいっぱいに設定
                ),
                rx.button(
                    rx.chakra.image(
                        src="start.png",
                        width="90%",
                        loading="lazy",
                        border_radius="50px",
                        border="5px solid black",
                    ),
                    on_click=ButtonState.start_game,
                    variant="ghost",
                    position="absolute",
                    bottom="7vh",  # 下からの位置を指定
                    left="50%",  # 左右中央に配置
                    transform="translateX(-50%)",  # 中央揃えの調整
                ),
                position="relative",  # 親要素に相対位置を設定
                width="100%",
                height="100vh",  # 画面の高さいっぱいに設定
            ),
            rx.cond(
                ButtonState.game_active,
                rx.flex(
                    rx.heading(f"Score: {ButtonState.score}", font_size="2em"),
                    rx.heading(f"Time: {ButtonState.time_remaining}", font_size="2em"),
                    justify="between",
                    padding="20px",
                    color="white",
                    bg="black",
                ),
            ),
        ),
        rx.script("""
            var button_sfx = new Audio("/button_se.mp3")
            var button_sfx2 = new Audio("/button_se2.mp3")
            var penalty_sfx = new Audio("/penalty_se.mp3")
            var bgm = new Audio("/bgm.mp3")
            function playFromStart(sfx) {
                if (sfx === 'button_sfx') {
                    button_sfx.currentTime = 0;
                    button_sfx.play();
                } else if (sfx === 'button_sfx2') {
                    button_sfx2.currentTime = 0;
                    button_sfx2.play();
                } else if (sfx === 'penalty_sfx') {
                    penalty_sfx.currentTime = 0;
                    penalty_sfx.play();
                }
            }
            function playBGM() {
                bgm.currentTime = 0;
                bgm.play();
            }
            function stopBGM() {
                bgm.pause();
                bgm.currentTime = 0;
            }
        """),
        rx.cond(
            ButtonState.game_active,
            rx.box(
                rx.foreach(
                    ButtonState.button_visibility,
                    button,
                ),
                special_button(),
                penalty_button(),
                overflow="hidden",
            ),
            rx.cond(
                ButtonState.time_remaining == 0,
                rx.center(
                    rx.vstack(
                        rx.chakra.image(
                            src="game_over.webp",
                            width="50%",
                            border_radius="full",
                        ),
                        rx.heading(
                            f"Final Score: {ButtonState.score}", font_size="2em"
                        ),
                        rx.button(
                            rx.chakra.image(
                                src="retry.png", width="30%", border_radius="60px"
                            ),
                            variant="ghost",
                            on_click=ButtonState.start_game,
                        ),
                        align="center",
                        spacing="5",
                    ),
                    height="100vh",
                    justify="center",
                ),
            ),
        ),
        position="relative",
        width="100vw",
        height="100vh",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",
        style={
            "background_color": "mint",
        },
    ),
    head_components=[
        rx.el.link(
            rel="manifest", href="/manifest.json", crossorigin="use-credentials"
        ),
        rx.script(src="scripts/loading_service_worker.js"),
        rx.script(src="scripts/freeze_window.js"),
    ],
)
