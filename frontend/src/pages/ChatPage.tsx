import React from 'react';
import { Menu, X } from 'lucide-react';
import { useStore } from '../store';
import { Sidebar } from '../components/Sidebar';
import { MessageList } from '../components/MessageList';
import { ChatInput } from '../components/ChatInput';
import { conversationApi } from '../services/api';

export const ChatPage: React.FC = () => {
  const {
    isSidebarOpen,
    toggleSidebar,
    setConversations,
    error,
    setError,
  } = useStore();

  React.useEffect(() => {
    const loadConversations = async () => {
      try {
        const response = await conversationApi.list();
        setConversations(response.items);
      } catch (error) {
        console.error('Error loading conversations:', error);
        // Don't show error on initial load, just log it
        // setError('Failed to load conversations');
      }
    };

    loadConversations();
  }, [setConversations, setError]);

  return (
    <div className="flex h-screen" style={{ backgroundColor: 'var(--color-background-primary)' }}>
      {/* Sidebar */}
      <div
        className="transition-all duration-300"
        style={{
          width: isSidebarOpen ? '280px' : '0',
          overflow: 'hidden',
        }}
      >
        <Sidebar />
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div
          className="flex items-center gap-3 px-4 py-3 border-b"
          style={{
            backgroundColor: 'var(--color-background-secondary)',
            borderColor: 'var(--color-border)',
          }}
        >
          <button
            onClick={toggleSidebar}
            className="p-2 rounded transition-colors"
            style={{ color: 'var(--color-text-primary)' }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'var(--color-background-hover)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'transparent';
            }}
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          <h1 className="text-lg font-semibold" style={{ color: 'var(--color-text-primary)' }}>
            PilotX
          </h1>
        </div>

        {/* Error Banner */}
        {error && (
          <div
            className="px-4 py-3 text-sm flex items-center justify-between"
            style={{
              backgroundColor: 'var(--color-error)',
              color: 'var(--color-text-inverse)',
            }}
          >
            <span>{error}</span>
            <button
              onClick={() => setError(null)}
              className="ml-4 px-2 py-1 rounded font-medium"
              style={{
                backgroundColor: 'rgba(0, 0, 0, 0.2)',
              }}
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Messages */}
        <MessageList />

        {/* Input */}
        <ChatInput />
      </div>
    </div>
  );
};
