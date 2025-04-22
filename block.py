# Tetris block implementation

import constants
import pygame
import math
import copy

class Block(object):
    """Class for handling tetris blocks"""    

    def __init__(self, shape, x, y, screen, color, rotate_en):
        """
        Initialize a tetris block.

        Parameters:
            shape - list of relative [x,y] coordinates for the block pieces
            x - initial x coordinate
            y - initial y coordinate
            screen - pygame surface to draw on
            color - RGB color tuple
            rotate_en - whether rotation is allowed
        """
        # Convert shape coordinates to Rect objects
        self.shape = []
        for sh in shape:
            bx = sh[0]*constants.BWIDTH + x
            by = sh[1]*constants.BHEIGHT + y
            block = pygame.Rect(bx, by, constants.BWIDTH, constants.BHEIGHT)
            self.shape.append(block)     
        
        self.rotate_en = rotate_en
        self.x = x
        self.y = y
        self.diffx = 0
        self.diffy = 0
        self.screen = screen
        self.color = color
        self.diff_rotation = 0

    def draw(self):
        """Draw the block on the screen."""
        for bl in self.shape:
            pygame.draw.rect(self.screen, self.color, bl)
            pygame.draw.rect(self.screen, constants.BLACK, bl, constants.MESH_WIDTH)
        
    def get_rotated(self, x, y):
        """
        Calculate rotated coordinates using transformation matrix.
        
        Parameters:
            x, y - coordinates to transform
        
        Returns:
            tuple of transformed (x, y) coordinates
        """
        rads = self.diff_rotation * (math.pi / 180.0)
        newx = x*math.cos(rads) - y*math.sin(rads)
        newy = y*math.cos(rads) + x*math.sin(rads)
        return (newx, newy)        

    def move(self, x, y):
        """
        Move block by the specified offset.
        
        Parameters:
            x, y - amount to move in each direction
        """
        self.diffx += x
        self.diffy += y  
        self._update()

    def remove_blocks(self, y):
        """
        Remove blocks at given Y coordinate and move blocks above down.
        
        Parameters:
            y - Y coordinate to clear
        """
        new_shape = []
        for shape_i in range(len(self.shape)):
            tmp_shape = self.shape[shape_i]
            if tmp_shape.y < y:
                # Block is above y, move down
                new_shape.append(tmp_shape)  
                tmp_shape.move_ip(0, constants.BHEIGHT)
            elif tmp_shape.y > y:
                # Block is below y, keep position
                new_shape.append(tmp_shape)
                
        self.shape = new_shape

    def has_blocks(self):
        """Return True if block contains any remaining pieces."""
        return len(self.shape) > 0

    def rotate(self):
        """Rotate the block 90 degrees if rotation is enabled."""
        if self.rotate_en:
            self.diff_rotation = 90
            self._update()

    def _update(self):
        """Update position of all pieces after rotation or movement."""
        for bl in self.shape:
            # Calculate new position based on original coordinates
            origX = (bl.x - self.x) / constants.BWIDTH
            origY = (bl.y - self.y) / constants.BHEIGHT
            rx, ry = self.get_rotated(origX, origY)
            newX = rx * constants.BWIDTH + self.x + self.diffx
            newY = ry * constants.BHEIGHT + self.y + self.diffy
            
            # Apply the movement
            newPosX = newX - bl.x
            newPosY = newY - bl.y
            bl.move_ip(newPosX, newPosY)
            
        # Update block's position and reset movement variables
        self.x += self.diffx
        self.y += self.diffy
        self.diffx = 0
        self.diffy = 0
        self.diff_rotation = 0

    def backup(self):
        """Save current block state."""
        self.shape_copy = copy.deepcopy(self.shape)
        self.x_copy = self.x
        self.y_copy = self.y
        self.rotation_copy = self.diff_rotation     

    def restore(self):
        """Restore block to previous saved state."""
        self.shape = self.shape_copy
        self.x = self.x_copy
        self.y = self.y_copy
        self.diff_rotation = self.rotation_copy

    def check_collision(self, rect_list):
        """
        Check for collision with provided rectangles.
        
        Parameters:
            rect_list - list of pygame Rect objects
        
        Returns:
            True if collision detected, False otherwise
        """
        for blk in rect_list:
            collist = blk.collidelistall(self.shape)
            if len(collist):
                return True
        return False
