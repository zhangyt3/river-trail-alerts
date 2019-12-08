import pytest

from scrape.scraper import parse_html


def test_parse_html():
    raw = """
    <!DOCTYPE html>
    <html lang="en-ca">
    <head>
        <title>Test Skating Trail Conditions Page</title>
    </head>
    <body>
        <ul>
            <li>
                <svg class="svg-icon closed"></svg>
                Rink Under the Canopy
            </li>
            <li>
                <svg class="svg-icon check"></svg>
                Hockey Rink at CN Stage
            </li>
        </ul>
        <ul>
            <li>
                <svg class="svg-icon dash"></svg>
                The Forks Port Rink
            </li>
            <li>
              <svg class="svg-icon check"></svg>
              The Forks Port to Queen Elizabeth Way
            </li>
        </ul>
        <ul>
            <li>
                <svg class="not-a-status"></svg>
                Blah
            </li>
        </ul>
    </body>
    </html>
    """
    statuses = parse_html(raw)
    assert len(statuses) == 4
    
    locations = [
        'Rink Under the Canopy',
        'Hockey Rink at CN Stage',
        'The Forks Port Rink',
        'The Forks Port to Queen Elizabeth Way'
    ]
    for loc in locations:
        assert loc in statuses

    assert statuses['Rink Under the Canopy'] == 'closed'
    assert statuses['Hockey Rink at CN Stage'] == 'open'
    assert statuses['The Forks Port Rink'] == 'conditions variable'
    assert statuses['The Forks Port to Queen Elizabeth Way'] == 'open'

    assert 'Blah' not in statuses


