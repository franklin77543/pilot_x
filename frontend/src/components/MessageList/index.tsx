import React from 'react';
import { useStore } from '../../store';
import { messageApi } from '../../services/api';
import { Message } from '../Message';

export const MessageList: React.FC = () => {
  const { messages, currentConversation, setMessages, setError } = useStore();
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    const loadMessages = async () => {
      if (!currentConversation) {
        setMessages([]);
        return;
      }

      try {
        const msgs = await messageApi.list(currentConversation.id);
        setMessages(msgs);
      } catch (error) {
        setError('Failed to load messages');
        console.error('Error loading messages:', error);
      }
    };

    loadMessages();
  }, [currentConversation, setMessages, setError]);

  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (!currentConversation) {
    return (
      <div
        className="flex-1 flex items-center justify-center"
        style={{ color: 'var(--color-text-secondary)' }}
      >
        <div className="text-center">
          <p className="text-lg mb-2">Welcome to PilotX</p>
          <p className="text-sm">Select a conversation or start a new chat</p>
        </div>
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div
        className="flex-1 flex items-center justify-center"
        style={{ color: 'var(--color-text-secondary)' }}
      >
        <div className="text-center">
          <p className="text-lg mb-2">No messages yet</p>
          <p className="text-sm">Start the conversation below</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto">
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};
