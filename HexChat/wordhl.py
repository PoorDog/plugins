import hexchat

__module_name__ = 'wordhl'
__module_author__ = 'TingPing'
__module_version__ = '1'
__module_description__ = 'Highlights some words of importance and copies the message to a separate tab'
# When you want to notice something, but not really get 'highlighted'

hlwords = ('hexchat', )
edited = False

# TAB_NAME is customizable
TAB_NAME = '(Highlights)'


def find_highlighttab():
    context = hexchat.find_context(channel=TAB_NAME)
    if context is None:
        hexchat.command('newserver -noconnect {0}'.format(TAB_NAME))
        return hexchat.find_context(channel=TAB_NAME)
    else:
        return context


def print_cb(word, word_eol, event, attr):
    global edited
    channel = hexchat.get_info('channel')
    highlight_context = find_highlighttab()

    # Ignore our own events, bouncer playback, empty messages
    if edited or attr.time or not len(word) > 1:
        return

    if any(_word in word[1] for _word in hlwords):
        word = [(word[i] if len(word) > i else '') for i in range(4)]
        msg = word[1]

        for _word in hlwords:
            msg = msg.replace(_word, '\00319' + _word + '\00399').strip()  # Color green

        edited = True
        hexchat.emit_print(event, word[0], msg, word[2], word[3])
        edited = False

        hexchat.command('gui color 3')

        if event == 'Channel Message':
            highlight_context.prnt('{0}\t\00318<{5}{4}{2}>\017 {1}'.format(channel, msg, *word))
        elif event == 'Channel Action':
            highlight_context.prnt('{0}\t\00318*\002{5}{4}{2}\017 {1}'.format(channel, msg, *word))

        return hexchat.EAT_ALL


hexchat.hook_print_attrs('Channel Message', print_cb, 'Channel Message', priority=hexchat.PRI_HIGHEST)
hexchat.hook_print_attrs('Channel Action', print_cb, 'Channel Action', priority=hexchat.PRI_HIGHEST)
