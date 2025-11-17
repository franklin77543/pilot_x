import React from 'react';
import { Send } from 'lucide-react';
import { useStore } from '../../store';
import { messageApi, conversationApi } from '../../services/api';

export const ChatInput: React.FC = () => {
  const {
    currentConversation,
    setCurrentConversation,
    addConversation,
    addMessage,
    isLoading,
    setLoading,
    setError,
    currentModel,
  } = useStore();

  const [input, setInput] = React.useState('');
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setLoading(true);
    setError(null);

    // Create temporary user message to display immediately
    const tempUserMessage = {
      id: `temp-${Date.now()}`,
      conversation_id: currentConversation?.id || '',
      role: 'user' as const,
      content: userMessage,
      created_at: new Date().toISOString(),
    };

    // Add user message to UI immediately
    addMessage(tempUserMessage);

    try {
      // Create conversation if needed
      let conversationId = currentConversation?.id;
      
      if (!conversationId) {
        const newConversation = await conversationApi.create();
        setCurrentConversation(newConversation);
        addConversation(newConversation);
        conversationId = newConversation.id;
      }

      // Send message and get AI response
      const assistantMessage = await messageApi.send(conversationId, {
        content: userMessage,
        model: currentModel?.id,
      });

      // Add the assistant's message
      addMessage(assistantMessage);
    } catch (error) {
      setError('Failed to send message');
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  React.useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  return (
    <div
      className="border-t p-4"
      style={{
        backgroundColor: 'var(--color-background-secondary)',
        borderColor: 'var(--color-border)',
      }}
    >
      <div className="max-w-4xl mx-auto">
        <form onSubmit={handleSubmit} className="flex gap-3 items-end">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
            disabled={isLoading}
            rows={1}
            className="flex-1 px-4 py-3 rounded-lg resize-none transition-colors"
            style={{
              backgroundColor: 'var(--color-background-tertiary)',
              color: 'var(--color-text-primary)',
              border: '1px solid var(--color-border)',
              maxHeight: '200px',
              outline: 'none',
            }}
            onFocus={(e) => {
              e.currentTarget.style.borderColor = 'var(--color-border-focus)';
            }}
            onBlur={(e) => {
              e.currentTarget.style.borderColor = 'var(--color-border)';
            }}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="px-4 py-3 rounded-lg transition-colors flex items-center gap-2 font-medium"
            style={{
              backgroundColor: input.trim() && !isLoading
                ? 'var(--color-primary)'
                : 'var(--color-background-hover)',
              color: input.trim() && !isLoading
                ? 'var(--color-text-inverse)'
                : 'var(--color-text-secondary)',
              cursor: input.trim() && !isLoading ? 'pointer' : 'not-allowed',
            }}
            onMouseEnter={(e) => {
              if (input.trim() && !isLoading) {
                e.currentTarget.style.backgroundColor = 'var(--color-primary-hover)';
              }
            }}
            onMouseLeave={(e) => {
              if (input.trim() && !isLoading) {
                e.currentTarget.style.backgroundColor = 'var(--color-primary)';
              }
            }}
          >
            {isLoading ? (
              <>
                <div className="animate-pulse">Sending...</div>
              </>
            ) : (
              <>
                <Send size={18} />
                <span>Send</span>
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};
