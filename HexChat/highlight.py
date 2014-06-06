import hexchat

__module_name__ = 'Highlight Logger'
__module_version__ = '2'
__module_description__ = 'Prints highlights to another tab'
# Forked from Arnavion's

TAB_NAME = '(Highlights)'

def find_highlighttab():
	context = hexchat.find_context(channel=TAB_NAME)
	if context == None:
		hexchat.command('newserver -noconnect {0}'.format(TAB_NAME))
		return hexchat.find_context(channel=TAB_NAME)
	else:
		return context

def highlight_callback(word, word_eol, user_data):	
	word = [(word[i] if len(word) > i else '') for i in range(4)]	
	highlight_context = find_highlighttab()	
	channel = hexchat.get_info('channel')
	
	if user_data == 'Channel Msg Hilight':
		highlight_context.prnt('{0}\t\00320<{4}{3}{1}>\017 {2}'.format(channel, *word))
	elif user_data == 'Channel Action Hilight':
		highlight_context.prnt('{0}\t\00320*\002{4}{3}{1}\017 {2}'.format(channel, *word))	

	highlight_context.command('gui color 3')
	
	return hexchat.EAT_NONE

find_highlighttab()
hexchat.hook_print('Channel Msg Hilight', highlight_callback, 'Channel Msg Hilight')
hexchat.hook_print('Channel Action Hilight', highlight_callback, 'Channel Action Hilight')

hexchat.prnt('Highlight Logger loaded')