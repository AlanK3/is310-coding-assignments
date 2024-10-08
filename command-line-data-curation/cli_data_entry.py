import csv
from rich.console import Console
from rich.table import Table

console = Console()

def InitialData():
    table = Table(title="Video Games")
    table.add_column("Title", style="yellow")
    table.add_column("Publishers", style="magenta", no_wrap=True)
    table.add_column("Year", justify="right")
    
    table.add_row("Tetris", "Alexey Pajitnov", "1984")
    table.add_row("Grand Theft Auto V", "Rockstar Games", "2013")
    table.add_row("Minecraft", "Mojang", "2009")
    
    console.print("Here is some initial data:", style="bold green")
    console.print(table)

def GatherData():
    game_data = []
    
    while True:
        title = console.input("[bold green]Enter the title of the video game: [/bold green]")
        publisher = console.input("[bold green]Enter the game's publisher: [/bold green]")
        year = console.input("[bold green]Enter the release year year: [/bold green]")
        
        # Show entered data for confirmation
        console.print(f"\n[bold]You entered:[/bold] \nTitle: {title}\nPublisher: {publisher}\nYear: {year}")
        confirmation = console.input("[bold green]Is this information correct? (Y/N): [/bold green]").lower()
        
        if confirmation == "y":
            game_data.append((title, publisher, year))
            add_more = console.input("[bold green]Do you want to add another game? (Y/N): [/bold green]").lower()
            if add_more == "n":
                break
        else:
            console.print("[bold red]Re-enter the game details.[/bold red]")
    
    return game_data

def SaveCSV(game_data, file_path="fav_video_games.csv"):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Publisher", "Year"])
        writer.writerows(game_data)
    
    console.print(f"[bold green]Data has been saved to {file_path}[/bold green]")

# Main program
def main():
    InitialData()
    
    console.print("\n[bold green]Now I want you to enter your favorite video games:[/bold green]")
    game_data = GatherData()
    
    SaveCSV(game_data)

if __name__ == "__main__":
    main()
