package jianyuebot

import (
	"fmt"

	"github.com/bwmarrin/discordgo"
)

func main() {
	dg, err := discordgo.New("Bot" + "Token")
	if err != nil {
		fmt.Println("Unable to establish discord session", err)
	}

	dg.AddHandler(messageCreate)

	dg.Identify.Intents = discordgo.IntentsGuildMessages
}
